import os
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()

AI_PROVIDER = os.getenv("AI_PROVIDER", "")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "claude-3-5-haiku-20241022")

SYSTEM_PROMPT = """You are NexBot, the AI assistant for Nexxus Tech — a specialized IT security consulting firm.
Nexxus Tech specializes in:
- Web Application Firewalls (WAF): Citrix NetScaler WAF, F5 BIG-IP, API protection
- Application Delivery Controllers: NetScaler ADC, load balancing, SSL offload
- Zero-Trust Architecture: combining NetScaler, Okta, Azure AD, DUO
- Cloud Security: AWS, Azure, multicloud security architectures
- AI-driven infrastructure automation

You are knowledgeable, professional, and helpful. Keep responses concise and focused on security, networking, and infrastructure topics.
Always recommend consulting with Nexxus Tech experts for complex implementations."""


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
    configured: bool


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # If not yet configured, return a friendly placeholder
    if not AI_API_KEY or not AI_PROVIDER:
        last_msg = request.messages[-1].content if request.messages else ""
        return ChatResponse(
            reply=(
                "Hi! I'm NexBot, Nexxus Tech's AI assistant. "
                "I'm not fully configured yet, but our team is ready to help you with "
                "WAF, NetScaler, Zero-Trust, and cloud security questions. "
                "Please use the contact form or email contact@nexxus-tech.com directly!"
            ),
            configured=False,
        )

    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    try:
        if AI_PROVIDER == "anthropic":
            return await _call_anthropic(messages)
        elif AI_PROVIDER == "openai":
            return await _call_openai(messages)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported AI provider: {AI_PROVIDER}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")


async def _call_anthropic(messages: list[dict]) -> ChatResponse:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": AI_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": AI_MODEL,
                "max_tokens": 1024,
                "system": SYSTEM_PROMPT,
                "messages": messages,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return ChatResponse(reply=data["content"][0]["text"], configured=True)


async def _call_openai(messages: list[dict]) -> ChatResponse:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {AI_API_KEY}", "content-type": "application/json"},
            json={
                "model": AI_MODEL,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
                "max_tokens": 1024,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return ChatResponse(reply=data["choices"][0]["message"]["content"], configured=True)
