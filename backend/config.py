from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    environment: str = "production"
    cors_origins: str = "https://nexxus-tech.com,https://www.nexxus-tech.com"
    jwt_secret_key: str = Field(default="", validation_alias="JWT_SECRET_KEY")
    encryption_key: str = Field(default="", validation_alias="ENCRYPTION_KEY")
    mongodb_uri: str = Field(
        default="mongodb://mongodb:27017/licensing",
        validation_alias="MONGODB_URI",
    )
    ai_provider: str = Field(default="", validation_alias="AI_PROVIDER")
    ai_api_key: str = Field(default="", validation_alias="AI_API_KEY")
    ai_model: str = Field(default="deepseek-chat", validation_alias="AI_MODEL")
    deepseek_base_url: str = Field(
        default="https://api.deepseek.com",
        validation_alias="DEEPSEEK_BASE_URL",
    )


settings = Settings()
