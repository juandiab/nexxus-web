from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies import get_db
from schemas.sync import (
    SyncDeactivatedResponse,
    SyncExpiredResponse,
    SyncRequest,
    SyncSuccessResponse,
)
from services.sync_service import (
    SyncCodeMismatchError,
    SyncDeactivatedError,
    SyncExpiredError,
    SyncNotFoundError,
    sync_license,
)

router = APIRouter(prefix="/sync", tags=["sync"])


async def _run_sync(
    db: AsyncIOMotorDatabase,
    *,
    app_fingerprint: str,
    app_name: str,
    license_code: str | None,
) -> SyncSuccessResponse:
    try:
        result = await sync_license(
            db,
            app_fingerprint=app_fingerprint,
            app_name=app_name,
            license_code=license_code,
        )
    except SyncNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No license found for this deployment.",
        ) from exc
    except SyncCodeMismatchError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="License code does not match this deployment.",
        ) from exc
    except SyncDeactivatedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=SyncDeactivatedResponse().model_dump(),
        ) from exc
    except SyncExpiredError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=SyncExpiredResponse(
                message=exc.message,
                licenseType=exc.license_type,
                expirationDate=exc.expiration_date,
            ).model_dump(mode="json"),
        ) from exc

    return SyncSuccessResponse(
        status=result.status,
        message=result.message,
        renewalCount=result.renewal_count,
        licenseType=result.license_type,
        registrationDate=result.registration_date,
        expirationDate=result.expiration_date,
        validityDays=result.validity_days,
        encryptedLicense=result.encrypted_license,
    )


@router.get("", response_model=SyncSuccessResponse)
async def get_sync_license(
    appfingerprint: str = Query(..., min_length=1, max_length=256),
    appname: str = Query(..., min_length=1, max_length=128),
    licensecode: str | None = Query(default=None, max_length=64),
    activationdate: str | None = Query(default=None, max_length=64),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> SyncSuccessResponse:
    _ = activationdate
    return await _run_sync(
        db,
        app_fingerprint=appfingerprint.strip(),
        app_name=appname.strip(),
        license_code=licensecode,
    )


@router.post("", response_model=SyncSuccessResponse)
async def post_sync_license(
    payload: SyncRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> SyncSuccessResponse:
    return await _run_sync(
        db,
        app_fingerprint=payload.appFingerprint.strip(),
        app_name=payload.appName.strip(),
        license_code=payload.licenseCode,
    )
