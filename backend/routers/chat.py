import json
import os
import re

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from models.chat import (
    ALLOWED_CRITICALITY,
    ALLOWED_ENQUIRY_TYPES,
    ALLOWED_SERVICES,
    ALLOWED_TECHNOLOGIES,
    ChatOptionsResponse,
    ChatRequest,
    ChatResponse,
    ChatSubmitRequest,
    ChatSubmitResponse,
)
from routers.contact import deliver_jpbot_enquiry

router = APIRouter()

AI_PROVIDER = os.getenv("AI_PROVIDER", "").strip().lower()
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

DISCOVERY_BASE_PROMPT = """You are JPbot, the intake assistant on nexxus-tech.com for Nexxus Tech.

The visitor completed a structured intake form. Their profile is in the first message — do NOT ask for contact, service, or technology fields again.

YOUR JOB:
1. Ask at most **two** short follow-up questions total in discovery, then offer to submit.
2. Acknowledge what they already said before asking something new.
3. Set ready_to_submit to **true** when:
   - You have enough for a consultant (scope, timeline, or problem summary), OR
   - They say they have nothing more to add, OR
   - They ask to send / finish / what else you need.

EFFICIENCY RULES (critical):
- **Never repeat** the same or similar question. Read the full thread first.
- If they answer "not at the moment", "nothing else", "that's all", etc. → thank them and set ready_to_submit true.
- Do not keep asking for "more scope" after they already gave scale, timeline, or platforms.
- Prefer: "We have enough to start — please use **Send enquiry to Nexxus**" over another question.

OTHER RULES:
- No pricing, contracts, or legal advice. A human consultant follows up.
- Under 80 words. Use **bold** and *italic* only (no headings, links, code).
- Match enquiry type — no incident language for new projects.

OUTPUT: ONLY valid JSON with non-empty reply:
{"reply": "message to visitor", "ready_to_submit": false}"""

TYPE_DISCOVERY_RULES: dict[str, str] = {
    "Troubleshooting / incident": """
ENQUIRY TYPE: Troubleshooting / incident (production or urgent breakage).
- Ask about symptoms, errors, impact, recent changes, and logs if needed.
- Use words like issue, outage, error, failure, impact.
- Do NOT ask about project goals or RFP-style success criteria unless they mention a planned change.""",
    "Support request": """
ENQUIRY TYPE: Support request (existing environment, not necessarily down).
- Ask what they need help with, current setup, and desired outcome.
- Balance troubleshooting and guidance; avoid assuming total outage.""",
    "New project / implementation": """
ENQUIRY TYPE: New project / implementation (migration, rollout, greenfield).
- NOT an incident. Never ask to "describe the issue" or "symptoms".
- If they gave migration type + timeline + scale (e.g. MPX, VIPs, datacenters, November) → set ready_to_submit true.
- Only ask ONE missing critical item (timeline OR scale OR cutover window), not the same category twice.""",
    "Assessment / discovery": """
ENQUIRY TYPE: Assessment / discovery (evaluate options, architecture review, quote).
- Ask what to assess, current state, constraints, stakeholders, and decision timeline.
- Do NOT use incident language unless they report an active outage.""",
    "General enquiry": """
ENQUIRY TYPE: General enquiry.
- Clarify what they need from Nexxus; stay neutral until intent is clear.""",
}

SUBMIT_READY_REPLY = (
    "We have **enough to get started** — thank you. Please tap **Send enquiry to Nexxus** below. "
    "Our team will review this thread and email you if anything else is needed."
)

DECLINE_PATTERN = re.compile(
    r"(not at the moment|nothing else|no more to add|that's all|that's it|"
    r"don't have (anything )?else|do not have (anything )?else|"
    r"what else\b|what else do you need|what else do you want|"
    r"no additional|can't share more|cannot share more|"
    r"that's everything|all i know|not right now|n/a)",
    re.IGNORECASE,
)

SUMMARY_SYSTEM_PROMPT = """Summarize a JPbot intake chat for Nexxus Tech.
Output ONLY valid JSON (no markdown, no ** bold **):
{
  "situation": "2-4 plain sentences",
  "pain_points": ["point one", "point two"],
  "urgency": "one plain sentence",
  "next_steps": ["action for Nexxus team"],
  "visitor_summary": "2-4 friendly sentences using you/your summarizing what the visitor reported"
}"""


def _discovery_system_prompt(profile) -> str:
    rules = TYPE_DISCOVERY_RULES.get(
        profile.enquiry_type,
        TYPE_DISCOVERY_RULES["General enquiry"],
    )
    return f"{DISCOVERY_BASE_PROMPT}\n\n{rules}"


def _profile_context(profile) -> str:
    techs = ", ".join(profile.technologies)
    if profile.technology_other:
        extra = f"Other: {profile.technology_other}"
        techs = f"{techs}, {extra}" if techs else extra
    return (
        "Visitor profile (already collected — do not ask again):\n"
        f"- Enquiry type: {profile.enquiry_type}\n"
        f"- Name: {profile.name}\n"
        f"- Email: {profile.email}\n"
        f"- Company: {profile.company or '(not provided)'}\n"
        f"- Service: {profile.service}\n"
        f"- Criticality: {profile.criticality}\n"
        f"- Users affected: {profile.users_affected}\n"
        f"- Technologies: {techs or '(none)'}\n"
        f"- Platform version: {profile.platform_version or '(not provided)'}\n"
        f"- Platform model: {profile.platform_model or '(not provided)'}\n"
    )


def _sanitize_history(messages: list) -> list[dict]:
    return [{"role": m.role, "content": m.content} for m in messages]


def _parse_discovery_response(raw: str) -> tuple[str, bool]:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            reply = str(data.get("reply", "")).strip()
            ready = bool(data.get("ready_to_submit", False))
            if reply:
                return reply[:MAX_REPLY_LEN], ready
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass
    match = re.search(r'"reply"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
    if match:
        reply = match.group(1).replace("\\n", "\n").replace('\\"', '"').strip()
        ready = '"ready_to_submit": true' in text.lower() or "'ready_to_submit': true" in text.lower()
        if reply:
            return reply[:MAX_REPLY_LEN], ready
    if text and not text.startswith("{"):
        return text[:MAX_REPLY_LEN], False
    return "", False


def _normalize_text(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()


def _last_user_text(history: list[dict]) -> str:
    for m in reversed(history):
        if m.get("role") == "user":
            return str(m.get("content", ""))
    return ""


def _user_turn_count(history: list[dict]) -> int:
    return sum(1 for m in history if m.get("role") == "user")


def _user_declined_more(history: list[dict]) -> bool:
    return bool(DECLINE_PATTERN.search(_last_user_text(history)))


def _enough_discovery_context(history: list[dict]) -> bool:
    users = [str(m.get("content", "")) for m in history if m.get("role") == "user"]
    if not users:
        return False
    combined = " ".join(users).lower()
    if len(users) >= 2 and sum(len(u) for u in users) >= 20:
        return True
    signals = (
        "migration",
        "mpx",
        "vip",
        "f5",
        "netscaler",
        "november",
        "datacenter",
        "timeline",
        "month",
        "appliance",
        "rollout",
        "deploy",
    )
    hits = sum(1 for s in signals if s in combined)
    return hits >= 2 or (len(users[0]) >= 35 and hits >= 1)


def _is_repetitive_reply(history: list[dict], reply: str) -> bool:
    norm_new = _normalize_text(reply)
    if not norm_new:
        return False
    prior = [m["content"] for m in history if m.get("role") == "assistant"]
    for prev in prior[-4:]:
        norm_prev = _normalize_text(prev)
        if norm_prev == norm_new:
            return True
        if len(norm_new) > 30 and norm_new in norm_prev:
            return True
    return False


def _finalize_discovery(
    reply: str, ready: bool, history: list[dict], enquiry_type: str
) -> tuple[str, bool]:
    if _user_declined_more(history):
        return SUBMIT_READY_REPLY, True
    if _enough_discovery_context(history):
        ready = True
    if _user_turn_count(history) >= 3:
        ready = True
    if reply and _is_repetitive_reply(history, reply):
        return SUBMIT_READY_REPLY, True
    if not reply:
        if ready or _enough_discovery_context(history) or _user_turn_count(history) >= 2:
            return SUBMIT_READY_REPLY, True
        return (
            "Thanks — what is the **one thing** our team should know first about your request?",
            False,
        )
    if ready and "send enquiry" not in reply.lower():
        reply = f"{reply}\n\nTap **Send enquiry to Nexxus** when you are ready."
    return reply[:MAX_REPLY_LEN], ready


MAX_REPLY_LEN = 4000


def _placeholder_reply() -> ChatResponse:
    return ChatResponse(
        reply=(
            "Hi! I'm JPbot. I'm not fully connected yet — please use our contact form "
            "or email contact@nexxus-tech.com and we'll help you right away."
        ),
        configured=False,
        ready_to_submit=False,
    )


async def _call_deepseek(
    *,
    system: str,
    messages: list[dict],
    json_mode: bool = False,
    max_tokens: int = 1024,
) -> str:
    payload: dict = {
        "model": AI_MODEL,
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": max_tokens,
        "temperature": 0.35,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    async with httpx.AsyncClient(timeout=45) as client:
        resp = await client.post(
            f"{DEEPSEEK_BASE_URL.rstrip('/')}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


def _format_transcript(messages: list) -> str:
    lines = []
    for m in messages:
        label = "Visitor" if m.role == "user" else "JPbot"
        lines.append(f"{label}: {m.content}")
    return "\n".join(lines)


@router.get("/chat/options", response_model=ChatOptionsResponse)
async def chat_options():
    return ChatOptionsResponse(
        services=ALLOWED_SERVICES,
        criticality=ALLOWED_CRITICALITY,
        technologies=ALLOWED_TECHNOLOGIES,
        enquiry_types=ALLOWED_ENQUIRY_TYPES,
    )


@router.get("/chat/services")
async def list_services():
    return {"services": ALLOWED_SERVICES}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Conversation history is required")

    if AI_PROVIDER != "deepseek" or not AI_API_KEY:
        return _placeholder_reply()

    history = _sanitize_history(request.messages)
    enquiry_type = request.profile.enquiry_type

    try:
        raw = await _call_deepseek(
            system=_discovery_system_prompt(request.profile),
            messages=[
                {"role": "user", "content": _profile_context(request.profile)},
                *history,
            ],
            json_mode=True,
        )
        reply, ready = _parse_discovery_response(raw)
        reply, ready = _finalize_discovery(reply, ready, history, enquiry_type)
        return ChatResponse(reply=reply, configured=True, ready_to_submit=ready)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}") from e


@router.post("/chat/submit", response_model=ChatSubmitResponse)
async def submit_chat(request: ChatSubmitRequest):
    if len(request.messages) < 1:
        raise HTTPException(
            status_code=400,
            detail="Please share a few details about your enquiry before submitting.",
        )

    transcript = _format_transcript(request.messages)
    parsed = {
        "situation": "The visitor submitted a JPbot enquiry.",
        "pain_points": [],
        "urgency": request.profile.criticality,
        "next_steps": ["Contact the visitor promptly."],
        "visitor_summary": (
            f"You asked about {request.profile.service}. Our team will review your details and follow up shortly."
        ),
    }

    if AI_PROVIDER == "deepseek" and AI_API_KEY:
        try:
            raw = await _call_deepseek(
                system=SUMMARY_SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"{_profile_context(request.profile)}\n\n"
                            f"Conversation:\n{transcript}"
                        ),
                    }
                ],
                json_mode=True,
                max_tokens=900,
            )
            parsed = _parse_summary_json(raw)
        except httpx.HTTPError:
            pass

    try:
        result = await deliver_jpbot_enquiry(
            request.profile,
            situation=str(parsed.get("situation", "")),
            pain_points=[str(p) for p in parsed.get("pain_points", []) if p],
            urgency=str(parsed.get("urgency", request.profile.criticality)),
            next_steps=[str(s) for s in parsed.get("next_steps", []) if s],
            visitor_summary=str(parsed.get("visitor_summary", "")),
            transcript=transcript,
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors()) from e

    return ChatSubmitResponse(success=result.success, message=result.message)


def _parse_summary_json(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    cleaned = re.sub(r"\*+", "", text)
    return {
        "situation": cleaned[:800] or "See conversation transcript.",
        "pain_points": [],
        "urgency": "Not specified.",
        "next_steps": ["Review transcript and contact the visitor."],
        "visitor_summary": (
            "We received your enquiry and our team is reviewing the details you shared via JPbot."
        ),
    }
