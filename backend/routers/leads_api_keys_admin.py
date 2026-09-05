from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from dependencies.auth import require_admin
from models.leads_api_key import LeadsApiKey, LeadsApiKeyCreate, LeadsApiKeyCreated
from services.leads_api_keys_store import (
    LeadsApiKeyNotFoundError,
    create_api_key,
    list_api_keys,
    revoke_api_key,
    rotate_api_key,
)
from services.leads_store import get_lead_proposal, get_proposal_file_path

router = APIRouter(tags=["leads-admin-ext"])


@router.get("/admin/leads-api-keys", response_model=list[LeadsApiKey])
async def get_leads_api_keys(_: dict = Depends(require_admin)) -> list[LeadsApiKey]:
    return await list_api_keys()


@router.post("/admin/leads-api-keys", response_model=LeadsApiKeyCreated, status_code=status.HTTP_201_CREATED)
async def post_leads_api_key(
    data: LeadsApiKeyCreate,
    auth: dict = Depends(require_admin),
) -> LeadsApiKeyCreated:
    created_by = auth.get("username") or "admin"
    raw_key, key = await create_api_key(data, created_by=created_by)
    return LeadsApiKeyCreated(
        id=key.id,
        name=key.name,
        key_prefix=key.key_prefix,
        agent=key.agent,
        scopes=key.scopes,
        api_key=raw_key,
        created_at=key.created_at,
    )


@router.post("/admin/leads-api-keys/{key_id}/revoke", response_model=LeadsApiKey)
async def post_revoke_leads_api_key(
    key_id: str,
    _: dict = Depends(require_admin),
) -> LeadsApiKey:
    try:
        return await revoke_api_key(key_id)
    except LeadsApiKeyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found") from exc


@router.post("/admin/leads-api-keys/{key_id}/rotate", response_model=LeadsApiKeyCreated)
async def post_rotate_leads_api_key(
    key_id: str,
    auth: dict = Depends(require_admin),
) -> LeadsApiKeyCreated:
    created_by = auth.get("username") or "admin"
    try:
        raw_key, _, new_key = await rotate_api_key(key_id, created_by=created_by)
    except LeadsApiKeyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found") from exc
    return LeadsApiKeyCreated(
        id=new_key.id,
        name=new_key.name,
        key_prefix=new_key.key_prefix,
        agent=new_key.agent,
        scopes=new_key.scopes,
        api_key=raw_key,
        created_at=new_key.created_at,
    )


@router.get("/admin/leads/{lead_id}/proposals/{proposal_id}/file")
async def download_lead_proposal_file(
    lead_id: str,
    proposal_id: str,
    _: dict = Depends(require_admin),
) -> FileResponse:
    proposal = await get_lead_proposal(lead_id, proposal_id)
    if not proposal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")

    path = get_proposal_file_path(lead_id, proposal_id)
    if not path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal file not found")

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=proposal.filename,
    )
