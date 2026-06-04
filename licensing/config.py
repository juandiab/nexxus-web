import sys

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "production"
    cors_origins: str = "https://nexxus-tech.com,https://www.nexxus-tech.com"

    admin_console_user: str = Field(validation_alias="ADMIN_CONSOLE_USER")
    admin_console_password: str = Field(validation_alias="ADMIN_CONSOLE_PASSWORD")
    admin_console_url: str = Field(
        default="https://nexxus-tech.com/adminconsole",
        validation_alias="ADMIN_CONSOLE_URL",
    )
    encryption_key: str = Field(validation_alias="ENCRYPTION_KEY")
    jwt_secret_key: str = Field(validation_alias="JWT_SECRET_KEY")
    mongodb_uri: str = Field(
        default="mongodb://mongodb:27017/licensing",
        validation_alias="MONGODB_URI",
    )

    jwt_expire_hours: int = 12

    smtp_host: str = Field(default="smtp.gmail.com", validation_alias="SMTP_HOST")
    smtp_port: int = Field(default=587, validation_alias="SMTP_PORT")
    smtp_user: str = Field(default="", validation_alias="SMTP_USER")
    smtp_pass: str = Field(default="", validation_alias="SMTP_PASS")
    smtp_from: str = Field(default="", validation_alias="CONTACT_FROM")
    email_log_only: bool = Field(default=True, validation_alias="EMAIL_LOG_ONLY")

    webauthn_rp_id: str = Field(default="nexxus-tech.com", validation_alias="WEBAUTHN_RP_ID")
    webauthn_rp_name: str = Field(default="Nexxus Tech Admin", validation_alias="WEBAUTHN_RP_NAME")
    webauthn_origin: str = Field(
        default="https://nexxus-tech.com",
        validation_alias="WEBAUTHN_ORIGIN",
    )

    @field_validator("admin_console_user", "admin_console_password", "encryption_key", "jwt_secret_key")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def webauthn_origins(self) -> list[str]:
        origins = set(self.cors_origin_list)
        origins.add(self.webauthn_origin.strip())
        return sorted(origins)


try:
    settings = Settings()
except ValidationError as exc:
    print(
        "Licensing service: missing or invalid environment variables.\n"
        "Add to /opt/nexxus-web/.env (see .env.example):\n"
        "  ADMIN_CONSOLE_USER, ADMIN_CONSOLE_PASSWORD,\n"
        "  ENCRYPTION_KEY (Fernet key), JWT_SECRET_KEY, MONGODB_URI\n",
        file=sys.stderr,
    )
    print(exc, file=sys.stderr)
    raise SystemExit(1) from exc
