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
