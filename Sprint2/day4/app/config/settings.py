from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    token_secret_key: str = "dev-secret-key"
    token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    token_algorithm: str = "HS256"
    allowed_cors_origins: str = "http://localhost:3000"
    api_version: str = "v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
