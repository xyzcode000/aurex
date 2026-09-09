from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================================================
    # APPLICATION
    # =========================================================

    app_name: str = "Aurex API"
    app_version: str = "0.1.0"

    # =========================================================
    # ENVIRONMENT
    # =========================================================

    environment: str = "development"
    debug: bool = False

    # =========================================================
    # DATABASE
    # =========================================================

    database_url: str = "sqlite:///./aurex.db"

    # =========================================================
    # SECURITY
    # =========================================================

    # Will be used when JWT authentication is implemented.
    secret_key: str = "CHANGE_THIS_IN_ENVIRONMENT"

    # JWT configuration
    access_token_expire_minutes: int = 30

    # =========================================================
    # PYDANTIC SETTINGS
    # =========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()