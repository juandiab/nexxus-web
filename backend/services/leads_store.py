from datetime import UTC, datetime
from math import ceil
from pathlib import Path

import aiofiles
from config import settings
from db import get_database
from models.lead import (
    DEFAULT_OWNER,
    Lead,
    LeadCreate,
    LeadIngestCreate,
    LeadIngestUpdate,
    LeadListPage,
    LeadNoteCreate,
    LeadProposal,
    LeadUpdate,
    TimelineEvent,
    WebFormLeadInput,
    new_lead_id,
    new_proposal_id,
)
from services.text_sanitize import sanitize_text

COLLECTION = "leads"
_index_ready = False
PROPOSALS_DIR = Path("/app/data/lead-proposals")
MAX_PROPOSAL_BYTES = 10 * 1024 * 1024

_SERVICE_PACKAGE_MAP = {
    "diagnostic": "diagnostic",
    "diagnóstico": "diagnostic",
    "pilot": "pilot",
    "piloto": "pilot",
    "system": "system",
    "sistema": "system",
    "retainer": "retainer",
    "ai integration": "system",
    "consultoría de integración de ia": "diagnostic",
    "integración de ia": "diagnostic",
    "integracion de ia": "diagnostic",
}


def map_service_to_package(service: str) -> str:
    key = (service or "").strip().lower()
    if not key:
        return "unknown"
    for fragment, package in _SERVICE_PACKAGE_MAP.items():
        if fragment in key:
            return package
    return "unknown"


def _now() -> datetime:
    return datetime.now(UTC)


def _sanitize_lead_fields(data: dict) -> dict:
    for field in ("notes", "research_summary"):
        if field in data and data[field] is not None:
            data[field] = sanitize_text(str(data[field]))
    return data


def _normalize_email(email: str | None) -> str | None:
    if not email:
        return None
    return str(email).strip().lower()


def _normalize_company(name: str) -> str:
    return (name or "").strip().lower()


def _proposals_from_doc(raw: list | None) -> list[LeadProposal]:
    if not raw:
        return []
    return [LeadProposal.model_validate(item) for item in raw]


def _doc_to_lead(doc: dict) -> Lead:
    timeline_raw = doc.get("timeline") or []
    timeline = [TimelineEvent.model_validate(item) for item in timeline_raw]
    return Lead(
        id=str(doc["_id"]),
        company_name=doc.get("company_name") or "",
        website=doc.get("website") or "",
        contact_name=doc.get("contact_name") or "",
        contact_email=doc.get("contact_email") or None,
        contact_phone=doc.get("contact_phone") or "",
        country=doc.get("country") or "",
        locale=doc.get("locale") or "en",
        source=doc.get("source") or "manual",
        status=doc.get("status") or "new",
        package_interest=doc.get("package_interest") or "unknown",
        notes=doc.get("notes") or "",
        research_summary=doc.get("research_summary") or "",
        proposal_status=doc.get("proposal_status") or "none",
        proposal_sent_at=doc.get("proposal_sent_at"),
        owner=doc.get("owner") or DEFAULT_OWNER,
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
        last_touch_at=doc.get("last_touch_at") or doc.get("updated_at") or doc.get("created_at"),
        archived=bool(doc.get("archived")),
        utm_source=doc.get("utm_source") or "",
        utm_medium=doc.get("utm_medium") or "",
        utm_campaign=doc.get("utm_campaign") or "",
        utm_term=doc.get("utm_term") or "",
        utm_content=doc.get("utm_content") or "",
        timeline=timeline,
        idempotency_key=doc.get("idempotency_key"),
        external_id=doc.get("external_id"),
        proposals=_proposals_from_doc(doc.get("proposals")),
        last_api_sync_at=doc.get("last_api_sync_at"),
        last_api_agent=doc.get("last_api_agent"),
    )


async def _ensure_indexes() -> None:
    global _index_ready
    if _index_ready:
        return
    db = get_database()
    col = db[COLLECTION]
    await col.create_index("company_name")
    await col.create_index("contact_email")
    await col.create_index("status")
    await col.create_index("source")
    await col.create_index("locale")
    await col.create_index("created_at")
    await col.create_index("archived")
    await col.create_index("idempotency_key", unique=True, sparse=True)
    _index_ready = True


def admin_lead_url(lead_id: str) -> str:
    base = settings.admin_console_url.rstrip("/")
    return f"{base}/leads?id={lead_id}"


async def find_lead_by_idempotency_key(key: str) -> Lead | None:
    await _ensure_indexes()
    if not key.strip():
        return None
    db = get_database()
    doc = await db[COLLECTION].find_one({"idempotency_key": key.strip()})
    return _doc_to_lead(doc) if doc else None


async def find_lead_by_email_and_company(email: str, company_name: str) -> Lead | None:
    await _ensure_indexes()
    normalized_email = _normalize_email(email)
    normalized_company = _normalize_company(company_name)
    if not normalized_email or not normalized_company:
        return None
    db = get_database()
    doc = await db[COLLECTION].find_one(
        {
            "contact_email": normalized_email,
            "company_name": {"$regex": f"^{company_name.strip()}$", "$options": "i"},
            "archived": {"$ne": True},
        }
    )
    if doc:
        return _doc_to_lead(doc)
    cursor = db[COLLECTION].find(
        {
            "contact_email": normalized_email,
            "archived": {"$ne": True},
        }
    )
    async for candidate in cursor:
        if _normalize_company(candidate.get("company_name") or "") == normalized_company:
            return _doc_to_lead(candidate)
    return None


async def ingest_create_lead(
    data: LeadIngestCreate,
    *,
    agent: str,
) -> tuple[Lead, bool, bool]:
    """Returns (lead, is_existing_match, is_idempotent_replay)."""
    await _ensure_indexes()
    if data.idempotency_key:
        existing = await find_lead_by_idempotency_key(data.idempotency_key)
        if existing:
            return existing, False, True

    if data.contact_email and data.company_name:
        existing = await find_lead_by_email_and_company(data.contact_email, data.company_name)
        if existing:
            return existing, True, False

    now = _now()
    lead_id = new_lead_id()
    payload = _sanitize_lead_fields(
        {
            "company_name": data.company_name.strip(),
            "website": data.website.strip(),
            "contact_name": data.contact_name.strip(),
            "contact_email": _normalize_email(data.contact_email),
            "contact_phone": data.contact_phone.strip(),
            "country": data.country.strip(),
            "locale": data.locale,
            "source": "api",
            "status": data.status,
            "package_interest": data.package_interest,
            "research_summary": data.research_summary,
            "notes": data.notes,
            "owner": DEFAULT_OWNER,
            "external_id": data.external_id,
            "idempotency_key": data.idempotency_key,
            "last_api_sync_at": now,
            "last_api_agent": agent,
            "proposals": [],
        }
    )

    timeline = [
        {
            "type": "created",
            "at": now,
            "detail": f"Lead created via API ({agent})",
            "by": agent,
        }
    ]

    if data.note.strip():
        note_text = sanitize_text(data.note)
        timeline.append(
            {
                "type": "note_added",
                "at": now,
                "detail": note_text,
                "by": agent,
            }
        )
        payload["notes"] = note_text

    doc = {
        "_id": lead_id,
        **payload,
        "archived": False,
        "proposal_status": "none",
        "proposal_sent_at": None,
        "created_at": now,
        "updated_at": now,
        "last_touch_at": now,
        "timeline": timeline,
    }
    db = get_database()
    await db[COLLECTION].insert_one(doc)
    return _doc_to_lead(doc), False, False


async def ingest_update_lead(
    lead_id: str,
    data: LeadIngestUpdate,
    *,
    agent: str,
) -> Lead | None:
    await _ensure_indexes()
    db = get_database()
    existing = await db[COLLECTION].find_one({"_id": lead_id})
    if not existing:
        return None

    note = (data.note or "").strip()
    updates = _sanitize_lead_fields(
        {
            k: v
            for k, v in data.model_dump(exclude_unset=True, exclude={"note"}).items()
            if v is not None
        }
    )
    if "contact_email" in updates and updates["contact_email"]:
        updates["contact_email"] = _normalize_email(str(updates["contact_email"]))

    now = _now()
    timeline = list(existing.get("timeline") or [])
    old_status = existing.get("status")
    new_status = updates.get("status")
    if new_status and new_status != old_status:
        timeline.append(
            {
                "type": "status_changed",
                "at": now,
                "detail": f"Status changed from {old_status} to {new_status}",
                "by": agent,
            }
        )

    old_proposal = existing.get("proposal_status")
    new_proposal = updates.get("proposal_status")
    if new_proposal == "sent" and new_proposal != old_proposal:
        timeline.append(
            {
                "type": "proposal_sent",
                "at": now,
                "detail": "Proposal marked as sent",
                "by": agent,
            }
        )
        if "proposal_sent_at" not in updates:
            updates["proposal_sent_at"] = now

    if note:
        note_text = sanitize_text(note)
        timeline.append(
            {
                "type": "note_added",
                "at": now,
                "detail": note_text,
                "by": agent,
            }
        )
        existing_notes = existing.get("notes") or ""
        updates["notes"] = f"{existing_notes}\n\n[{now.isoformat()}] {note_text}".strip()

    updates["updated_at"] = now
    updates["last_touch_at"] = now
    updates["last_api_sync_at"] = now
    updates["last_api_agent"] = agent
    updates["timeline"] = timeline

    if not updates:
        return _doc_to_lead(existing)

    await db[COLLECTION].update_one({"_id": lead_id}, {"$set": updates})
    doc = await db[COLLECTION].find_one({"_id": lead_id})
    return _doc_to_lead(doc) if doc else None


async def search_leads_paginated(
    *,
    company: str = "",
    email: str = "",
    status: str | None = None,
    page: int = 1,
    limit: int = 20,
) -> LeadListPage:
    await _ensure_indexes()
    query: dict = {"archived": {"$ne": True}}
    if status:
        query["status"] = status
    if email.strip():
        query["contact_email"] = _normalize_email(email.strip())
    if company.strip():
        query["company_name"] = {"$regex": company.strip(), "$options": "i"}

    safe_limit = max(1, min(limit, 100))
    safe_page = max(1, page)
    skip = (safe_page - 1) * safe_limit

    db = get_database()
    col = db[COLLECTION]
    total = await col.count_documents(query)
    cursor = col.find(query).sort("created_at", -1).skip(skip).limit(safe_limit)
    items: list[Lead] = []
    async for doc in cursor:
        items.append(_doc_to_lead(doc))

    pages = ceil(total / safe_limit) if total else 0
    return LeadListPage(
        items=items,
        page=safe_page,
        limit=safe_limit,
        total=total,
        pages=pages,
    )


async def add_lead_proposal(
    lead_id: str,
    *,
    file_bytes: bytes,
    filename: str,
    kind: str,
    language: str,
    email_subject: str = "",
    email_body: str = "",
    notes: str = "",
    mark_sent: bool = False,
    agent: str,
) -> LeadProposal | None:
    await _ensure_indexes()
    if len(file_bytes) > MAX_PROPOSAL_BYTES:
        raise ValueError("Proposal PDF exceeds 10 MB limit")

    db = get_database()
    existing = await db[COLLECTION].find_one({"_id": lead_id})
    if not existing:
        return None

    proposal_id = new_proposal_id()
    lead_dir = PROPOSALS_DIR / lead_id
    lead_dir.mkdir(parents=True, exist_ok=True)
    storage_path = lead_dir / f"{proposal_id}.pdf"

    async with aiofiles.open(storage_path, "wb") as handle:
        await handle.write(file_bytes)

    now = _now()
    proposal = LeadProposal(
        id=proposal_id,
        kind=kind,
        language=language,
        filename=filename or f"{proposal_id}.pdf",
        storage_path=str(storage_path),
        email_subject=sanitize_text(email_subject),
        email_body=sanitize_text(email_body),
        notes=sanitize_text(notes),
        uploaded_at=now,
        uploaded_by_agent=agent,
    )

    proposals = list(existing.get("proposals") or [])
    proposals.append(proposal.model_dump())

    updates: dict = {
        "proposals": proposals,
        "updated_at": now,
        "last_touch_at": now,
        "last_api_sync_at": now,
        "last_api_agent": agent,
    }

    current_proposal_status = existing.get("proposal_status") or "none"
    if kind == "draft" and current_proposal_status != "sent":
        updates["proposal_status"] = "draft"
    elif kind == "final" and mark_sent:
        updates["proposal_status"] = "sent"
        updates["proposal_sent_at"] = now
        timeline = list(existing.get("timeline") or [])
        timeline.append(
            {
                "type": "proposal_sent",
                "at": now,
                "detail": f"Final proposal uploaded and marked sent ({language})",
                "by": agent,
            }
        )
        updates["timeline"] = timeline
    elif kind == "final":
        if current_proposal_status != "sent":
            updates["proposal_status"] = "draft"

    await db[COLLECTION].update_one({"_id": lead_id}, {"$set": updates})
    return proposal


def get_proposal_file_path(lead_id: str, proposal_id: str) -> Path | None:
    path = PROPOSALS_DIR / lead_id / f"{proposal_id}.pdf"
    if path.is_file():
        return path
    return None


async def get_lead_proposal(lead_id: str, proposal_id: str) -> LeadProposal | None:
    lead = await get_lead(lead_id)
    if not lead:
        return None
    for proposal in lead.proposals:
        if proposal.id == proposal_id:
            return proposal
    return None


async def create_lead(data: LeadCreate, *, actor: str = "admin") -> Lead:
    await _ensure_indexes()
    now = _now()
    lead_id = new_lead_id()
    payload = _sanitize_lead_fields(data.model_dump())
    contact_email = payload.get("contact_email")
    if contact_email:
        payload["contact_email"] = str(contact_email).strip().lower()

    doc = {
        "_id": lead_id,
        **payload,
        "archived": False,
        "created_at": now,
        "updated_at": now,
        "last_touch_at": now,
        "timeline": [
            {
                "type": "created",
                "at": now,
                "detail": f"Lead created ({payload.get('source', 'manual')})",
                "by": actor,
            }
        ],
    }
    db = get_database()
    await db[COLLECTION].insert_one(doc)
    return _doc_to_lead(doc)


async def create_web_form_lead(data: WebFormLeadInput) -> Lead:
    """Create a lead from a public website form (source=web_form, status=new)."""
    create = LeadCreate(
        company_name=data.company_name.strip(),
        contact_name=data.contact_name.strip(),
        contact_email=data.contact_email,
        contact_phone=data.contact_phone.strip(),
        country=data.country.strip(),
        locale=data.locale,
        source="web_form",
        status="new",
        package_interest=data.package_interest,
        notes=sanitize_text(data.notes),
        owner=DEFAULT_OWNER,
        utm_source=data.utm_source.strip(),
        utm_medium=data.utm_medium.strip(),
        utm_campaign=data.utm_campaign.strip(),
        utm_term=data.utm_term.strip(),
        utm_content=data.utm_content.strip(),
    )
    return await create_lead(create, actor="web_form")


async def get_lead(lead_id: str) -> Lead | None:
    await _ensure_indexes()
    db = get_database()
    doc = await db[COLLECTION].find_one({"_id": lead_id})
    if not doc:
        return None
    return _doc_to_lead(doc)


async def list_leads(
    *,
    q: str = "",
    status: str | None = None,
    source: str | None = None,
    locale: str | None = None,
    include_archived: bool = False,
) -> list[Lead]:
    await _ensure_indexes()
    query: dict = {}
    if not include_archived:
        query["archived"] = {"$ne": True}
    if status:
        query["status"] = status
    if source:
        query["source"] = source
    if locale:
        query["locale"] = locale

    db = get_database()
    cursor = db[COLLECTION].find(query).sort("created_at", -1)
    leads: list[Lead] = []
    needle = q.strip().lower()
    async for doc in cursor:
        lead = _doc_to_lead(doc)
        if needle:
            haystack = " ".join(
                [
                    lead.company_name,
                    lead.contact_name,
                    lead.contact_email or "",
                    lead.website,
                ]
            ).lower()
            if needle not in haystack:
                continue
        leads.append(lead)
    return leads


async def update_lead(lead_id: str, data: LeadUpdate, *, actor: str = "admin") -> Lead | None:
    await _ensure_indexes()
    db = get_database()
    existing = await db[COLLECTION].find_one({"_id": lead_id})
    if not existing:
        return None

    updates = _sanitize_lead_fields(
        {k: v for k, v in data.model_dump(exclude_unset=True).items() if v is not None}
    )
    if "contact_email" in updates and updates["contact_email"]:
        updates["contact_email"] = str(updates["contact_email"]).strip().lower()

    if not updates:
        return _doc_to_lead(existing)

    now = _now()
    timeline = list(existing.get("timeline") or [])
    old_status = existing.get("status")
    new_status = updates.get("status")
    if new_status and new_status != old_status:
        timeline.append(
            {
                "type": "status_changed",
                "at": now,
                "detail": f"Status changed from {old_status} to {new_status}",
                "by": actor,
            }
        )

    old_proposal = existing.get("proposal_status")
    new_proposal = updates.get("proposal_status")
    if new_proposal == "sent" and new_proposal != old_proposal:
        timeline.append(
            {
                "type": "proposal_sent",
                "at": now,
                "detail": "Proposal marked as sent",
                "by": actor,
            }
        )
        if "proposal_sent_at" not in updates:
            updates["proposal_sent_at"] = now

    updates["updated_at"] = now
    updates["last_touch_at"] = now
    updates["timeline"] = timeline

    await db[COLLECTION].update_one({"_id": lead_id}, {"$set": updates})
    doc = await db[COLLECTION].find_one({"_id": lead_id})
    return _doc_to_lead(doc) if doc else None


async def add_lead_note(lead_id: str, data: LeadNoteCreate, *, actor: str = "admin") -> Lead | None:
    await _ensure_indexes()
    db = get_database()
    existing = await db[COLLECTION].find_one({"_id": lead_id})
    if not existing:
        return None

    now = _now()
    note_text = sanitize_text(data.note)
    timeline = list(existing.get("timeline") or [])
    timeline.append(
        {
            "type": "note_added",
            "at": now,
            "detail": note_text,
            "by": actor,
        }
    )

    existing_notes = existing.get("notes") or ""
    combined_notes = f"{existing_notes}\n\n[{now.isoformat()}] {note_text}".strip()

    await db[COLLECTION].update_one(
        {"_id": lead_id},
        {
            "$set": {
                "notes": combined_notes,
                "timeline": timeline,
                "updated_at": now,
                "last_touch_at": now,
            }
        },
    )
    doc = await db[COLLECTION].find_one({"_id": lead_id})
    return _doc_to_lead(doc) if doc else None


async def archive_lead(lead_id: str, *, actor: str = "admin") -> bool:
    await _ensure_indexes()
    db = get_database()
    existing = await db[COLLECTION].find_one({"_id": lead_id})
    if not existing:
        return False

    now = _now()
    timeline = list(existing.get("timeline") or [])
    timeline.append(
        {
            "type": "note_added",
            "at": now,
            "detail": "Lead archived",
            "by": actor,
        }
    )
    result = await db[COLLECTION].update_one(
        {"_id": lead_id},
        {
            "$set": {
                "archived": True,
                "updated_at": now,
                "last_touch_at": now,
                "timeline": timeline,
            }
        },
    )
    return result.modified_count > 0


async def export_leads_csv_rows(
    *,
    q: str = "",
    status: str | None = None,
    source: str | None = None,
    locale: str | None = None,
    include_archived: bool = False,
) -> list[dict]:
    leads = await list_leads(
        q=q,
        status=status,
        source=source,
        locale=locale,
        include_archived=include_archived,
    )
    rows: list[dict] = []
    for lead in leads:
        rows.append(
            {
                "id": lead.id,
                "company_name": lead.company_name,
                "website": lead.website,
                "contact_name": lead.contact_name,
                "contact_email": lead.contact_email or "",
                "contact_phone": lead.contact_phone,
                "country": lead.country,
                "locale": lead.locale,
                "source": lead.source,
                "status": lead.status,
                "package_interest": lead.package_interest,
                "proposal_status": lead.proposal_status,
                "proposal_sent_at": lead.proposal_sent_at.isoformat() if lead.proposal_sent_at else "",
                "owner": lead.owner,
                "created_at": lead.created_at.isoformat() if lead.created_at else "",
                "updated_at": lead.updated_at.isoformat() if lead.updated_at else "",
                "last_touch_at": lead.last_touch_at.isoformat() if lead.last_touch_at else "",
                "research_summary": lead.research_summary,
                "notes": lead.notes[:2000] if len(lead.notes) > 2000 else lead.notes,
                "utm_source": lead.utm_source,
                "utm_medium": lead.utm_medium,
                "utm_campaign": lead.utm_campaign,
            }
        )
    return rows
