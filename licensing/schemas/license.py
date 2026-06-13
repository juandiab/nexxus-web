from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_serializer

from models.license import LicenseType, LicenseStatus
from utils.time import ensure_utc_aware


class LicenseCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    email: EmailStr
    company: str = Field(default="", max_length=256)
    country: str = Field(default="", max_length=128)
    licenseType: LicenseType = "free"
    application: str = Field(min_length=1, max_length=128)
    validityDays: int | None = Field(default=None, ge=1, le=3650)


class LicenseUpdateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    email: EmailStr
    company: str = Field(default="", max_length=256)
    country: str = Field(default="", max_length=128)
    licenseType: LicenseType
    application: str = Field(min_length=1, max_length=128)
    validityDays: int = Field(ge=1, le=3650)


class LicenseExtendRequest(BaseModel):
    days: int = Field(ge=1, le=3650)


class LicenseTypeChangeRequest(BaseModel):
    licenseType: LicenseType
    recalculateValidity: bool = True


class LicenseResponse(BaseModel):
    id: str
    name: str
    email: str
    company: str
    country: str = ""
    registrationDate: datetime | None = None
    licenseType: LicenseType
    usageType: str | None = None
    application: str
    expirationDate: datetime | None = None
    validityDays: int | None = None
    active: bool = True
    renewalBlocked: bool = False
    status: LicenseStatus = "active"
    hasLicenseCode: bool = False
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    @field_serializer(
        "registrationDate",
        "expirationDate",
        "createdAt",
        "updatedAt",
        when_used="json",
    )
    def serialize_utc_datetime(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        aware = ensure_utc_aware(value)
        return aware.strftime("%Y-%m-%dT%H:%M:%SZ")


class LicenseCreatedResponse(LicenseResponse):
    licenseCode: str


class LicenseCodeResponse(BaseModel):
    licenseCode: str
