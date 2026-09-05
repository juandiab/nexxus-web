import secrets

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import settings
from models.leads_api_key import LeadsApiKey
from services.leads_api_keys_store import LeadsApiKeyLookupResult, lookup_api_key

security = HTTPBearer(auto_error=False)
LEADS_WRITE_SCOPE = "leads:write"


def _bootstrap_keys() -> frozenset[str]:
    keys: set[str] = set()
    primary = (settings.leads_api_key or "").strip()
    if primary:
        keys.add(primary)
    extra = (settings.leads_api_keys or "").strip()
    if extra:
        for part in extra.split(","):
            cleaned = part.strip()
            if cleaned:
                keys.add(cleaned)
    return frozenset(keys)


def _extract_bearer_key(
    credentials: HTTPAuthorizationCredentials | None,
) -> str | None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        return None
    token = credentials.credentials.strip()
    return token or None


def _extract_raw_key(
    credentials: HTTPAuthorizationCredentials | None,
    header_key: str | None,
) -> str | None:
    cleaned_header = (header_key or "").strip() or None
    bearer_key = _extract_bearer_key(credentials)
    return cleaned_header or bearer_key


async def _authenticate_leads_key(raw_key: str | None) -> tuple[LeadsApiKey | None, bool]:
    if not raw_key or not raw_key.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Leads API key",
        )

    key = raw_key.strip()
    lookup_result, db_key = await lookup_api_key(key)
    if lookup_result == LeadsApiKeyLookupResult.OK and db_key is not None:
        return db_key, False
    if lookup_result == LeadsApiKeyLookupResult.FORBIDDEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key lacks leads:write scope",
        )
    if lookup_result == LeadsApiKeyLookupResult.REVOKED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Leads API key",
        )

    bootstrap = _bootstrap_keys()
    if bootstrap:
        matched = any(secrets.compare_digest(key, candidate) for candidate in bootstrap)
        if matched:
            return None, True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Leads API key",
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Leads API is not configured — create a key in admin Settings",
    )


async def require_leads_write(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    x_nexxus_leads_key: str | None = Header(default=None, alias="X-Nexxus-Leads-Key"),
) -> dict:
    raw_key = _extract_raw_key(credentials, x_nexxus_leads_key)
    db_key, is_bootstrap = await _authenticate_leads_key(raw_key)

    if db_key is not None:
        if "leads:write" not in db_key.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API key lacks leads:write scope",
            )
        return {
            "scope": LEADS_WRITE_SCOPE,
            "agent": db_key.agent,
            "key_id": db_key.id,
            "bootstrap": False,
        }

    if is_bootstrap:
        return {
            "scope": LEADS_WRITE_SCOPE,
            "agent": "leads",
            "key_id": None,
            "bootstrap": True,
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid Leads API key",
    )


def resolve_leads_agent(
    auth: dict,
    x_nexxus_agent: str | None = Header(default=None, alias="X-Nexxus-Agent"),
) -> str:
    header_agent = (x_nexxus_agent or "").strip().lower()
    if header_agent in ("leads", "chief-of-staff"):
        return header_agent
    agent = auth.get("agent") or "leads"
    if agent in ("leads", "chief-of-staff"):
        return agent
    return "leads"
