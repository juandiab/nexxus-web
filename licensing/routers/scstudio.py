from fastapi import APIRouter, Depends, Header, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from dependencies import get_db, require_admin
from schemas.scstudio import (
    ScStudioApiKeyCreateRequest,
    ScStudioApiKeyCreatedResponse,
    ScStudioApiKeyPatchRequest,
    ScStudioApiKeyResponse,
    ScStudioApiKeySecretResponse,
    ScStudioApproveResponse,
    ScStudioMessageResponse,
    ScStudioRegenerateApiKeyResponse,
    ScStudioRegisterRequest,
    ScStudioRegisterResponse,
    ScStudioServerResponse,
    ScStudioSyncRequest,
    ScStudioSyncResponse,
)
from services.scstudio_service import (
    ScStudioApiKeyNotFoundError,
    ScStudioApiKeyUnavailableError,
    ScStudioInvalidStateError,
    ScStudioNotFoundError,
    ScStudioRegistrationConflictError,
    approve_server,
    create_api_key,
    delete_api_key,
    delete_server,
    get_api_key_secret,
    list_api_keys,
    list_servers,
    register_server,
    regenerate_api_key,
    reject_server,
    set_api_key_active,
    sync_license_database,
    validate_api_key,
)

router = APIRouter(prefix="/scstudio", tags=["scstudio"])


@router.post("/register", response_model=ScStudioRegisterResponse)
async def post_register(
    payload: ScStudioRegisterRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> ScStudioRegisterResponse:
    try:
        result = await register_server(
            db,
            server_name=payload.serverName,
            server_fingerprint=payload.serverFingerprint,
            ip_address=payload.ipAddress,
            public_ip_address=payload.publicIpAddress,
        )
    except ScStudioRegistrationConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A server with this fingerprint is already approved.",
        ) from exc

    return ScStudioRegisterResponse(
        registrationId=result["id"],
        status=result["status"],
    )


@router.post("/sync", response_model=ScStudioSyncResponse)
async def post_sync(
    payload: ScStudioSyncRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    x_scstudio_api_key: str | None = Header(default=None, alias="X-ScStudio-Api-Key"),
) -> ScStudioSyncResponse:
    if not x_scstudio_api_key or not x_scstudio_api_key.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-ScStudio-Api-Key header.",
        )

    try:
        auth = await validate_api_key(
            db,
            api_key=x_scstudio_api_key.strip(),
            server_id=payload.serverId,
        )
        result = await sync_license_database(
            db,
            server_fingerprint=auth["serverFingerprint"],
            server_id=auth["serverId"],
        )
    except ScStudioInvalidStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    return ScStudioSyncResponse(**result)


@router.get("/servers", response_model=list[ScStudioServerResponse])
async def get_servers(
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> list[ScStudioServerResponse]:
    return [ScStudioServerResponse(**row) for row in await list_servers(db)]


@router.post("/servers/{registration_id}/approve", response_model=ScStudioApproveResponse)
async def post_approve_server(
    registration_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(require_admin),
) -> ScStudioApproveResponse:
    try:
        server, api_key = await approve_server(
            db,
            registration_id,
            approved_by=current_user.get("username", "admin"),
        )
    except ScStudioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found.") from exc
    except ScStudioInvalidStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ScStudioApproveResponse(serverId=server["serverId"], apiKey=api_key)


@router.post("/servers/{registration_id}/reject", response_model=ScStudioServerResponse)
async def post_reject_server(
    registration_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> ScStudioServerResponse:
    try:
        server = await reject_server(db, registration_id)
    except ScStudioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found.") from exc
    except ScStudioInvalidStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ScStudioServerResponse(**server)


@router.delete("/servers/{registration_id}", response_model=ScStudioMessageResponse)
async def delete_server_route(
    registration_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> ScStudioMessageResponse:
    try:
        await delete_server(db, registration_id)
    except ScStudioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found.") from exc

    return ScStudioMessageResponse(message="Server registration deleted.")


@router.post("/servers/{registration_id}/regenerate-api-key", response_model=ScStudioRegenerateApiKeyResponse)
async def post_regenerate_api_key(
    registration_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(require_admin),
) -> ScStudioRegenerateApiKeyResponse:
    try:
        api_key, server = await regenerate_api_key(
            db,
            registration_id,
            created_by=current_user.get("username", "admin"),
        )
    except ScStudioNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found.") from exc
    except ScStudioInvalidStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ScStudioRegenerateApiKeyResponse(
        apiKeyId=server["apiKeyId"],
        keyPrefix=server["keyPrefix"],
        apiKey=api_key,
    )


@router.get("/api-keys", response_model=list[ScStudioApiKeyResponse])
async def get_api_keys(
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> list[ScStudioApiKeyResponse]:
    return [ScStudioApiKeyResponse(**row) for row in await list_api_keys(db)]


@router.post("/api-keys", response_model=ScStudioApiKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def post_api_key(
    payload: ScStudioApiKeyCreateRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(require_admin),
) -> ScStudioApiKeyCreatedResponse:
    try:
        api_key, key_row = await create_api_key(
            db,
            server_id=payload.serverId,
            created_by=current_user.get("username", "admin"),
        )
    except ScStudioInvalidStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ScStudioApiKeyCreatedResponse(
        id=key_row["id"],
        serverId=key_row["serverId"],
        apiKey=api_key,
        keyPrefix=key_row["keyPrefix"],
    )


@router.get("/api-keys/{key_id}/secret", response_model=ScStudioApiKeySecretResponse)
async def get_api_key_secret_route(
    key_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> ScStudioApiKeySecretResponse:
    try:
        row = await get_api_key_secret(db, key_id)
    except ScStudioApiKeyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.") from exc
    except ScStudioApiKeyUnavailableError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ScStudioApiKeySecretResponse(**row)


@router.patch("/api-keys/{key_id}", response_model=ScStudioApiKeyResponse)
async def patch_api_key(
    key_id: str,
    payload: ScStudioApiKeyPatchRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> ScStudioApiKeyResponse:
    try:
        row = await set_api_key_active(db, key_id, active=payload.active)
    except ScStudioApiKeyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.") from exc

    return ScStudioApiKeyResponse(**row)


@router.delete("/api-keys/{key_id}", response_model=ScStudioMessageResponse)
async def delete_api_key_route(
    key_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    _: dict = Depends(require_admin),
) -> ScStudioMessageResponse:
    try:
        await delete_api_key(db, key_id)
    except ScStudioApiKeyNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.") from exc

    return ScStudioMessageResponse(message="API key deleted.")
