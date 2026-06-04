from pydantic import BaseModel


class WebAuthnUsernameRequest(BaseModel):
    username: str


class WebAuthnStatusResponse(BaseModel):
    username: str
    exists: bool
    hasPasskey: bool
    passkeyRequired: bool
    canRegister: bool = False


class WebAuthnRegisterBeginRequest(BaseModel):
    username: str


class WebAuthnRegisterFinishRequest(BaseModel):
    username: str
    credential: dict
    label: str = ""


class WebAuthnLoginBeginRequest(BaseModel):
    username: str
    preferCrossDevice: bool = False


class WebAuthnLoginFinishRequest(BaseModel):
    username: str
    credential: dict
