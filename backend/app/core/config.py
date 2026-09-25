from pydantic import model_validator
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

    secret_key: str = "CHANGE_THIS_IN_ENVIRONMENT"

    access_token_expire_minutes: int = 30

    # =========================================================
    # CORS
    # =========================================================

    # Comma-separated origins.
    #
    # Example:
    #
    # CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
    #
    # Keep this explicit in production.
    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    # =========================================================
    # VALIDATION
    # =========================================================

    @model_validator(mode="after")
    def validate_security_configuration(self):
        """
        Prevent the application from starting in production
        with the development placeholder JWT secret.
        """

        environment = self.environment.strip().lower()

        if environment in {"production", "prod"}:
            if self.secret_key == "CHANGE_THIS_IN_ENVIRONMENT":
                raise ValueError(
                    "SECRET_KEY must be configured in production."
                )

            if len(self.secret_key) < 32:
                raise ValueError(
                    "SECRET_KEY must contain at least 32 characters "
                    "in production."
                )

        if self.access_token_expire_minutes <= 0:
            raise ValueError(
                "ACCESS_TOKEN_EXPIRE_MINUTES must be greater than zero."
            )

        if not self.cors_origins.strip():
            raise ValueError(
                "CORS_ORIGINS must contain at least one allowed origin."
            )

        return self

    # =========================================================
    # PYDANTIC SETTINGS
    # =========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()