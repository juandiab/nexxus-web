from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies import get_db, require_licensing_access
from schemas.auth import MessageResponse
from schemas.license import (
    LicenseCodeResponse,
    LicenseCreateRequest,
    LicenseCreatedResponse,
    LicenseExtendRequest,
    LicenseResponse,
    LicenseTypeChangeRequest,
    LicenseUpdateRequest,
)
from services.license_service import (
    change_license_type,
    create_license,
    delete_license,
    expire_license,
    extend_license,
    get_license_by_id,
    get_license_plain_code,
    list_licenses,
    set_license_active,
    update_license,
)
from services.license_notification_service import try_notify_license_change
from models.license import serialize_license

router = APIRouter(prefix="/licenses", tags=["licenses"])


@router.get("", response_model=list[LicenseResponse])
async def get_licenses(
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> list[LicenseResponse]:
    return [LicenseResponse(**row) for row in await list_licenses(db)]


@router.get("/{license_id}", response_model=LicenseResponse)
async def get_license(
    license_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseResponse:
    doc = await get_license_by_id(db, license_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    return LicenseResponse(**serialize_license(doc))


@router.get("/{license_id}/code", response_model=LicenseCodeResponse)
async def get_license_code(
    license_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseCodeResponse:
    code = await get_license_plain_code(db, license_id)
    if code is None:
        doc = await get_license_by_id(db, license_id)
        if doc is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No license code stored for this license",
        )
    return LicenseCodeResponse(licenseCode=code)


@router.post("", response_model=LicenseCreatedResponse, status_code=status.HTTP_201_CREATED)
async def post_license(
    payload: LicenseCreateRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseCreatedResponse:
    try:
        row, plain_code = await create_license(
            db,
            name=payload.name,
            email=payload.email,
            company=payload.company,
            license_type=payload.licenseType,
            application=payload.application,
            validity_days=payload.validityDays,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return LicenseCreatedResponse(**row, licenseCode=plain_code)


@router.put("/{license_id}", response_model=LicenseResponse)
async def put_license(
    license_id: str,
    payload: LicenseUpdateRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseResponse:
    try:
        updated = await update_license(
            db,
            license_id,
            name=payload.name,
            email=payload.email,
            company=payload.company,
            license_type=payload.licenseType,
            application=payload.application,
            validity_days=payload.validityDays,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    await try_notify_license_change(db, license_id, change="updated")
    return LicenseResponse(**updated)


@router.delete("/{license_id}", response_model=MessageResponse)
async def remove_license(
    license_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> MessageResponse:
    deleted = await delete_license(db, license_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    return MessageResponse(message="License deleted")


@router.post("/{license_id}/expire", response_model=LicenseResponse)
async def post_expire_license(
    license_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseResponse:
    updated = await expire_license(db, license_id)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    await try_notify_license_change(db, license_id, change="expired")
    return LicenseResponse(**updated)


@router.post("/{license_id}/deactivate", response_model=LicenseResponse)
async def post_deactivate_license(
    license_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseResponse:
    updated = await set_license_active(db, license_id, active=False)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    await try_notify_license_change(db, license_id, change="deactivated")
    return LicenseResponse(**updated)


@router.post("/{license_id}/reactivate", response_model=LicenseResponse)
async def post_reactivate_license(
    license_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseResponse:
    updated = await set_license_active(db, license_id, active=True)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    await try_notify_license_change(db, license_id, change="reactivated")
    return LicenseResponse(**updated)


@router.post("/{license_id}/extend", response_model=LicenseResponse)
async def post_extend_license(
    license_id: str,
    payload: LicenseExtendRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseResponse:
    updated = await extend_license(db, license_id, days=payload.days)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    await try_notify_license_change(
        db,
        license_id,
        change="extended",
        days_added=payload.days,
    )
    return LicenseResponse(**updated)


@router.post("/{license_id}/change-type", response_model=LicenseResponse)
async def post_change_license_type(
    license_id: str,
    payload: LicenseTypeChangeRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_licensing_access),
) -> LicenseResponse:
    try:
        updated = await change_license_type(
            db,
            license_id,
            license_type=payload.licenseType,
            recalculate_validity=payload.recalculateValidity,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    await try_notify_license_change(db, license_id, change="type_changed")
    return LicenseResponse(**updated)
