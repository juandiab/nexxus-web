from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "production"
    cors_origins: str = "https://nexxus-tech.com,https://www.nexxus-tech.com"

    admin_console_user: str
    admin_console_password: str
    encryption_key: str
    jwt_secret_key: str
    mongodb_uri: str = "mongodb://mongodb:27017/licensing"

    jwt_expire_hours: int = 12

    @field_validator("admin_console_user", "admin_console_password", "encryption_key", "jwt_secret_key")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v


settings = Settings()
