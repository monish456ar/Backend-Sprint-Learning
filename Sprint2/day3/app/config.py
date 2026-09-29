from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    token_secret_key: str
    token_expire_minutes: int
    allowed_cors_origins: str
    api_version: str
    # redis_url:str

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")


settings = Settings()
