from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, model_validator

from models.license import LicenseType, UsageType, LicenseStatus


class ActivationRequest(BaseModel):
    appFingerprint: str = Field(min_length=1, max_length=256)
    appName: str = Field(min_length=1, max_length=128)
    activationDate: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)
    email: EmailStr
    country: str = Field(min_length=1, max_length=128)
    company: str = Field(default="", max_length=256)
    usageType: UsageType

    @model_validator(mode="after")
    def company_required_for_org_use(self) -> "ActivationRequest":
        if self.usageType != "personal" and not self.company.strip():
            raise ValueError("Company is required for non-personal license use.")
        return self


class ActivationRequestResponse(BaseModel):
    email: str
    application: str
    licenseType: LicenseType
    usageType: UsageType
    validityDays: int
    otpExpiresAtUnix: int
    message: str = "License code and verification code sent to your email."


class ActivationVerifyRequest(BaseModel):
    appFingerprint: str = Field(min_length=1, max_length=256)
    appName: str = Field(min_length=1, max_length=128)
    email: EmailStr
    otp: str = Field(min_length=1, max_length=32)


class OfflineLicensePackage(BaseModel):
    format: str
    version: int
    algorithm: str
    appFingerprint: str
    appName: str
    licenseCode: str
    encryptedLicense: str
    exportedAt: str


class ActivationResponse(BaseModel):
    id: str
    name: str
    email: str
    country: str
    company: str
    application: str
    licenseType: LicenseType
    registrationDate: datetime | None = None
    expirationDate: datetime | None = None
    validityDays: int
    usageType: UsageType | None = None
    appFingerprint: str
    appName: str
    activationDate: str | None = None
    licenseCode: str | None = None
    offlineLicense: OfflineLicensePackage | None = None
    active: bool = True
    status: LicenseStatus | None = None
    message: str = "Email verified. Your license has been activated."


class ActivationExistingResponse(ActivationResponse):
    message: str = "This deployment already has an activated license."


class ActivationRecoverCheckResponse(BaseModel):
    found: bool
    email: str | None = None
    application: str | None = None
    name: str | None = None
    licenseType: LicenseType | None = None
    expirationDate: datetime | None = None


class ActivationRecoverRequest(BaseModel):
    appFingerprint: str = Field(min_length=1, max_length=256)
    appName: str = Field(min_length=1, max_length=128)
    activationDate: str = Field(min_length=1, max_length=64)
    email: EmailStr


class ActivationRecoverRequestResponse(BaseModel):
    email: str
    application: str
    name: str
    licenseType: LicenseType
    otpExpiresAtUnix: int
    message: str = "Verification code sent to your email to link this license to the device."


class ActivationRecoverVerifyRequest(BaseModel):
    appFingerprint: str = Field(min_length=1, max_length=256)
    appName: str = Field(min_length=1, max_length=128)
    email: EmailStr
    otp: str = Field(min_length=1, max_length=32)
