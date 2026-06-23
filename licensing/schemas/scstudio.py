from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ScStudioServerStatus = Literal["pending", "approved", "rejected"]


class ScStudioRegisterRequest(BaseModel):
    serverName: str = Field(min_length=1, max_length=256)
    serverFingerprint: str = Field(min_length=1, max_length=512)
    ipAddress: str = Field(min_length=1, max_length=128)
    publicIpAddress: str = Field(min_length=1, max_length=128)


class ScStudioRegisterResponse(BaseModel):
    registrationId: str
    status: ScStudioServerStatus


class ScStudioSyncRequest(BaseModel):
    serverId: str = Field(min_length=1, max_length=64)


class ScStudioSyncResponse(BaseModel):
    version: Literal[1] = 1
    algorithm: Literal["AES-256-GCM+HKDF-SHA256"] = "AES-256-GCM+HKDF-SHA256"
    serverId: str
    licenseCount: int
    syncedAt: datetime
    encryptedDatabase: str


class ScStudioServerResponse(BaseModel):
    id: str
    serverName: str
    serverFingerprint: str
    ipAddress: str
    publicIpAddress: str
    status: ScStudioServerStatus
    serverId: str | None = None
    approvedAt: datetime | None = None
    approvedBy: str | None = None
    rejectedAt: datetime | None = None
    lastSyncAt: datetime | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    apiKeyId: str | None = None
    keyPrefix: str | None = None
    apiKeyActive: bool | None = None
    apiKeyRetrievable: bool = False
    apiKeyLastUsedAt: datetime | None = None


class ScStudioApproveResponse(BaseModel):
    serverId: str
    apiKey: str
    message: str = "Server approved. Copy the API key and provide it to the SC Studio operator."


class ScStudioRegenerateApiKeyResponse(BaseModel):
    apiKeyId: str
    keyPrefix: str
    apiKey: str
    message: str = "API key regenerated. Copy it for the SC Studio operator."


class ScStudioApiKeyResponse(BaseModel):
    id: str
    serverId: str
    serverName: str
    keyPrefix: str
    active: bool
    retrievable: bool = False
    createdAt: datetime | None = None
    lastUsedAt: datetime | None = None
    createdBy: str | None = None


class ScStudioApiKeyCreatedResponse(BaseModel):
    id: str
    serverId: str
    apiKey: str
    keyPrefix: str
    message: str = "API key created. You can view or copy it from the API keys list."


class ScStudioApiKeyCreateRequest(BaseModel):
    serverId: str = Field(min_length=1, max_length=64)


class ScStudioApiKeyPatchRequest(BaseModel):
    active: bool


class ScStudioApiKeySecretResponse(BaseModel):
    id: str
    serverId: str
    serverName: str
    keyPrefix: str
    apiKey: str


class ScStudioMessageResponse(BaseModel):
    message: str
