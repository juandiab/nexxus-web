import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse

from dependencies.auth import require_admin
from models.lead import Lead, LeadCreate, LeadNoteCreate, LeadUpdate
from services.leads_store import (
    add_lead_note,
    archive_lead,
    create_lead,
    export_leads_csv_rows,
    get_lead,
    list_leads,
    update_lead,
)

router = APIRouter(prefix="/admin/leads", tags=["leads-admin"])

# Leads bot drafts proposals offline; update proposal_status when sent.
# Future automation: POST /api/admin/leads (create) and PATCH /api/admin/leads/{id} (partial update).


@router.get("", response_model=list[Lead])
async def get_leads(
    _: dict = Depends(require_admin),
    q: str = Query("", description="Search company name or email"),
    status: str | None = Query(None),
    source: str | None = Query(None),
    locale: str | None = Query(None),
    include_archived: bool = Query(False),
) -> list[Lead]:
    return await list_leads(
        q=q,
        status=status,
        source=source,
        locale=locale,
        include_archived=include_archived,
    )


@router.get("/export.csv")
async def export_leads_csv(
    _: dict = Depends(require_admin),
    q: str = Query(""),
    status: str | None = Query(None),
    source: str | None = Query(None),
    locale: str | None = Query(None),
    include_archived: bool = Query(False),
) -> StreamingResponse:
    rows = await export_leads_csv_rows(
        q=q,
        status=status,
        source=source,
        locale=locale,
        include_archived=include_archived,
    )
    buffer = io.StringIO()
    if rows:
        writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    else:
        buffer.write("id,company_name\n")

    filename = f"leads-{datetime.utcnow().strftime('%Y%m%d')}.csv"
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{lead_id}", response_model=Lead)
async def get_lead_detail(lead_id: str, _: dict = Depends(require_admin)) -> Lead:
    lead = await get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


@router.post("", response_model=Lead, status_code=status.HTTP_201_CREATED)
async def create_admin_lead(
    data: LeadCreate,
    auth: dict = Depends(require_admin),
) -> Lead:
    actor = auth.get("username") or "admin"
    return await create_lead(data, actor=actor)


@router.put("/{lead_id}", response_model=Lead)
async def update_admin_lead(
    lead_id: str,
    data: LeadUpdate,
    auth: dict = Depends(require_admin),
) -> Lead:
    actor = auth.get("username") or "admin"
    lead = await update_lead(lead_id, data, actor=actor)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


@router.patch("/{lead_id}", response_model=Lead)
async def patch_admin_lead(
    lead_id: str,
    data: LeadUpdate,
    auth: dict = Depends(require_admin),
) -> Lead:
    """Partial update for admin UI and future Leads bot automation."""
    actor = auth.get("username") or "admin"
    lead = await update_lead(lead_id, data, actor=actor)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


@router.post("/{lead_id}/notes", response_model=Lead)
async def add_admin_lead_note(
    lead_id: str,
    data: LeadNoteCreate,
    auth: dict = Depends(require_admin),
) -> Lead:
    actor = auth.get("username") or "admin"
    lead = await add_lead_note(lead_id, data, actor=actor)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def archive_admin_lead(lead_id: str, auth: dict = Depends(require_admin)) -> Response:
    actor = auth.get("username") or "admin"
    ok = await archive_lead(lead_id, actor=actor)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
