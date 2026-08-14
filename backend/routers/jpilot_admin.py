from fastapi import APIRouter, Depends

from dependencies.auth import require_admin
from models.contact import JpilotLead
from services.jpilot_leads import list_jpilot_leads

router = APIRouter(prefix="/admin/jpilot", tags=["jpilot-admin"])


@router.get("/leads", response_model=list[JpilotLead])
async def get_jpilot_leads(_: dict = Depends(require_admin)) -> list[JpilotLead]:
    return await list_jpilot_leads()
