from functools import lru_cache
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "VoiceSense API"
    api_prefix: str = "/v1"
    environment: str = "development"
    database_url: str = Field(default="postgresql+asyncpg://voicesense:voicesense@localhost:5432/voicesense")
    redis_url: str | None = None
    jwt_secret: str = Field(default="change-me-in-production")
    jwt_issuer: str = "voicesense"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    password_reset_minutes: int = 30
    email_verification_hours: int = 24
    session_cookie_name: str = "vs_session"
    csrf_cookie_name: str = "vs_csrf"
    allowed_origins: list[AnyHttpUrl] = []
    google_oauth_client_id: str | None = None
    google_oauth_client_secret: str | None = None
    google_oauth_redirect_uri: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()