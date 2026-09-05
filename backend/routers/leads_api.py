from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile, status

from dependencies.leads_auth import require_leads_write, resolve_leads_agent
from models.lead import Lead, LeadIngestCreate, LeadIngestResponse, LeadIngestUpdate, LeadListPage, LeadProposal
from services.leads_store import (
    admin_lead_url,
    get_lead,
    ingest_create_lead,
    ingest_update_lead,
    add_lead_proposal,
    search_leads_paginated,
)
from services.rate_limit import enforce_rate_limit

router = APIRouter(prefix="/v1/leads", tags=["leads-ingestion"])

# Leads bot drafts proposals offline; update proposal_status when sent.


@router.post("", response_model=LeadIngestResponse)
async def create_lead_via_api(
    request: Request,
    data: LeadIngestCreate,
    auth: dict = Depends(require_leads_write),
) -> LeadIngestResponse:
    enforce_rate_limit(request)
    agent = resolve_leads_agent(auth, request.headers.get("X-Nexxus-Agent"))
    lead, is_existing, is_idempotent = await ingest_create_lead(data, agent=agent)

    response = LeadIngestResponse(id=lead.id, admin_url=admin_lead_url(lead.id))
    if is_existing:
        response.existing = True
        return response

    if is_idempotent:
        return response

    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=response.model_dump(),
    )


@router.patch("/{lead_id}", response_model=Lead)
async def patch_lead_via_api(
    request: Request,
    lead_id: str,
    data: LeadIngestUpdate,
    auth: dict = Depends(require_leads_write),
) -> Lead:
    enforce_rate_limit(request)
    agent = resolve_leads_agent(auth, request.headers.get("X-Nexxus-Agent"))
    lead = await ingest_update_lead(lead_id, data, agent=agent)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


@router.get("", response_model=LeadListPage)
async def list_leads_via_api(
    request: Request,
    _: dict = Depends(require_leads_write),
    company: str = Query(""),
    email: str = Query(""),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
) -> LeadListPage:
    enforce_rate_limit(request)
    return await search_leads_paginated(
        company=company,
        email=email,
        status=status,
        page=page,
        limit=limit,
    )


@router.get("/{lead_id}", response_model=Lead)
async def get_lead_via_api(
    request: Request,
    lead_id: str,
    _: dict = Depends(require_leads_write),
) -> Lead:
    enforce_rate_limit(request)
    lead = await get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


@router.post("/{lead_id}/proposals", response_model=LeadProposal, status_code=status.HTTP_201_CREATED)
async def upload_lead_proposal(
    request: Request,
    lead_id: str,
    auth: dict = Depends(require_leads_write),
    file: UploadFile = File(...),
    kind: str = Form(...),
    language: str = Form(...),
    email_subject: str = Form(""),
    email_body: str = Form(""),
    notes: str = Form(""),
    mark_sent: bool = Form(False),
) -> LeadProposal:
    enforce_rate_limit(request)
    agent = resolve_leads_agent(auth, request.headers.get("X-Nexxus-Agent"))

    if kind not in ("draft", "final"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="kind must be draft or final")
    if language not in ("en", "es"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="language must be en or es")

    content_type = (file.content_type or "").lower()
    if content_type not in ("application/pdf", "application/x-pdf", "binary/octet-stream"):
        if not (file.filename or "").lower().endswith(".pdf"):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only PDF files are accepted")

    file_bytes = await file.read()
    if not file_bytes.startswith(b"%PDF"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid PDF file")

    try:
        proposal = await add_lead_proposal(
            lead_id,
            file_bytes=file_bytes,
            filename=file.filename or "proposal.pdf",
            kind=kind,
            language=language,
            email_subject=email_subject,
            email_body=email_body,
            notes=notes,
            mark_sent=mark_sent,
            agent=agent,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(exc)) from exc

    if not proposal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return proposal
