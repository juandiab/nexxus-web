from datetime import UTC, datetime

from db import get_database
from models.contact import JpilotInterestRequest

COLLECTION = "jpilotLeads"
_index_ready = False


async def _ensure_indexes() -> None:
    global _index_ready
    if _index_ready:
        return
    db = get_database()
    await db[COLLECTION].create_index("email", unique=True)
    await db[COLLECTION].create_index("createdAt")
    _index_ready = True


async def upsert_jpilot_lead(data: JpilotInterestRequest) -> None:
    await _ensure_indexes()
    now = datetime.now(UTC)
    email = str(data.email).strip().lower()
    db = get_database()
    await db[COLLECTION].update_one(
        {"email": email},
        {
            "$set": {
                "name": data.name,
                "email": email,
                "useType": data.use_type,
                "country": data.country,
                "company": data.company,
                "companySize": data.company_size,
                "updatedAt": now,
                "lastSeenAt": now,
            },
            "$setOnInsert": {"createdAt": now},
        },
        upsert=True,
    )


async def list_jpilot_leads() -> list[dict]:
    await _ensure_indexes()
    db = get_database()
    cursor = db[COLLECTION].find({}).sort("createdAt", -1)
    leads: list[dict] = []
    async for doc in cursor:
        leads.append(
            {
                "name": doc.get("name") or "",
                "email": doc.get("email") or "",
                "useType": doc.get("useType") or "",
                "country": doc.get("country") or "",
                "company": doc.get("company") or "",
                "companySize": doc.get("companySize") or "",
                "createdAt": doc.get("createdAt"),
                "updatedAt": doc.get("updatedAt"),
                "lastSeenAt": doc.get("lastSeenAt"),
            }
        )
    return leads
