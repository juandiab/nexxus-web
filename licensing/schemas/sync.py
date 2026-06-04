from datetime import datetime
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SyncRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    appFingerprint: str = Field(
        min_length=1,
        max_length=256,
        validation_alias=AliasChoices("appFingerprint", "appfingerprint"),
    )
    appName: str = Field(
        min_length=1,
        max_length=128,
        validation_alias=AliasChoices("appName", "appname"),
    )
    licenseCode: str | None = Field(
        default=None,
        max_length=64,
        validation_alias=AliasChoices("licenseCode", "licensecode"),
    )
    activationDate: str | None = Field(
        default=None,
        max_length=64,
        validation_alias=AliasChoices("activationDate", "activationdate"),
    )


class SyncSuccessResponse(BaseModel):
    version: Literal[1] = 1
    algorithm: Literal["AES-256-GCM+HKDF-SHA256"] = "AES-256-GCM+HKDF-SHA256"
    status: Literal["active", "renewed"]
    message: str = ""
    renewalCount: int = 0
    licenseType: str = "free"
    registrationDate: datetime | None = None
    expirationDate: datetime | None = None
    validityDays: int = 0
    encryptedLicense: str


class SyncExpiredResponse(BaseModel):
    status: Literal["expired"] = "expired"
    message: str
    licenseType: str
    expirationDate: datetime | None = None


class SyncDeactivatedResponse(BaseModel):
    status: Literal["deactivated"] = "deactivated"
    message: str = "License deactivated by administrator."
