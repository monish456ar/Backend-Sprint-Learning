from app.config import Settings, settings


def get_config() -> Settings:
    """Provides application configuration settings via dependency injection."""
    return settings
