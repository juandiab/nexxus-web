from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import ValidationError

from dependencies import get_db
from schemas.activation import (
    ActivationRequest,
    ActivationRequestResponse,
    ActivationResponse,
    ActivationVerifyRequest,
    OfflineLicensePackage,
)
from services.activation_service import request_activation, verify_activation_otp
from services.email_service import send_license_activation_email
from services.offline_license_service import get_offline_license_package, offline_license_filename

router = APIRouter(prefix="/activation", tags=["activation"])
activate_router = APIRouter(tags=["activation"])


def _deployment_query_string(params: dict[str, str]) -> str | None:
    fingerprint = (
        params.get("appfingerprint")
        or params.get("appFingerprint")
        or ""
    ).strip()
    app_name = (params.get("appname") or params.get("appName") or "").strip()
    activation_date = (
        params.get("activationdate")
        or params.get("activationDate")
        or ""
    ).strip()
    if not fingerprint or not app_name:
        return None
    query = urlencode(
        {
            "appfingerprint": fingerprint,
            "appname": app_name,
            "activationdate": activation_date,
        }
    )
    return query


def _redirect_to_activation_page(params: dict[str, str]) -> RedirectResponse:
    query = _deployment_query_string(params)
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing appfingerprint and appname. Open the activation page to enter your details.",
        )
    return RedirectResponse(url=f"/licensing/activate?{query}", status_code=303)


async def _parse_deployment_params(request: Request) -> dict[str, str]:
    content_type = request.headers.get("content-type", "").lower()
    params: dict[str, str] = {}

    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form = await request.form()
        for key, value in form.multi_items():
            if isinstance(value, str):
                params[key] = value
        return params

    raw = (await request.body()).decode("utf-8", errors="replace").strip()
    if not raw:
        return params

    if raw.startswith("{"):
        return params

    parsed = parse_qs(raw, keep_blank_values=True)
    for key, values in parsed.items():
        if values:
            params[key] = values[0]
    return params


async def _handle_activation_request(
    payload: ActivationRequest,
    db: AsyncIOMotorDatabase,
) -> ActivationRequestResponse:
    try:
        preview, plain_code, otp = await request_activation(
            db,
            app_fingerprint=payload.appFingerprint.strip(),
            app_name=payload.appName.strip(),
            activation_date=payload.activationDate.strip(),
            name=payload.name,
            email=payload.email,
            company=payload.company,
            country=payload.country,
            usage_type=payload.usageType,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    try:
        await send_license_activation_email(
            to_address=preview["email"],
            name=preview["name"],
            company=preview.get("company", ""),
            application=preview["application"],
            license_code=plain_code,
            otp_code=otp,
            license_type=preview["licenseType"],
            validity_days=preview["validityDays"],
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc

    return ActivationRequestResponse(
        email=preview["email"],
        application=preview["application"],
        licenseType=preview["licenseType"],
        usageType=preview["usageType"],
        validityDays=preview["validityDays"],
        otpExpiresAtUnix=preview["otpExpiresAtUnix"],
    )


@router.post("/request", response_model=ActivationRequestResponse, status_code=status.HTTP_200_OK)
async def post_activation_request(
    payload: ActivationRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> ActivationRequestResponse:
    return await _handle_activation_request(payload, db)


@activate_router.post("/activate")
async def post_activate_entry(
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """
    POST /licensing/activate supports two callers:

    1. JPilot (or HTML form) posting deployment params only → redirect to the
       activation page where the user enters name, email, and company.

    2. JSON API clients posting the full activation payload → start step 1
       (same as POST /licensing/activation/request).
    """
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        try:
            data = await request.json()
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON body.",
            ) from exc
        if not isinstance(data, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="JSON body must be an object.",
            )
        if not str(data.get("name", "")).strip() or not str(data.get("email", "")).strip():
            return _redirect_to_activation_page(
                {
                    "appfingerprint": str(data.get("appFingerprint") or data.get("appfingerprint") or ""),
                    "appname": str(data.get("appName") or data.get("appname") or ""),
                    "activationdate": str(data.get("activationDate") or data.get("activationdate") or ""),
                }
            )
        try:
            payload = ActivationRequest.model_validate(data)
        except ValidationError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.errors()) from exc
        return await _handle_activation_request(payload, db)

    params = await _parse_deployment_params(request)
    return _redirect_to_activation_page(params)


@router.post("/verify", response_model=ActivationResponse, status_code=status.HTTP_201_CREATED)
async def post_activation_verify(
    payload: ActivationVerifyRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> ActivationResponse:
    try:
        row = await verify_activation_otp(
            db,
            app_fingerprint=payload.appFingerprint.strip(),
            app_name=payload.appName.strip(),
            email=payload.email,
            otp=payload.otp.strip(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ActivationResponse(**row)


@router.get("/offline-license")
async def get_offline_license(
    appfingerprint: str = Query(..., min_length=1, max_length=256),
    appname: str = Query(..., min_length=1, max_length=128),
    email: str = Query(..., min_length=3, max_length=256),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> OfflineLicensePackage:
    try:
        package = await get_offline_license_package(
            db,
            app_fingerprint=appfingerprint.strip(),
            app_name=appname.strip(),
            email=email.strip().lower(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return OfflineLicensePackage(**package)


@router.get("/offline-license/download")
async def download_offline_license(
    appfingerprint: str = Query(..., min_length=1, max_length=256),
    appname: str = Query(..., min_length=1, max_length=128),
    email: str = Query(..., min_length=3, max_length=256),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> Response:
    try:
        package = await get_offline_license_package(
            db,
            app_fingerprint=appfingerprint.strip(),
            app_name=appname.strip(),
            email=email.strip().lower(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    filename = offline_license_filename(appname.strip(), package.get("exportedAt"))
    body = json.dumps(package, indent=2)
    return Response(
        content=body,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
