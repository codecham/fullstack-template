from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# The .env file at the repository root, two levels above apps/api.
# Inside Docker this file does not exist: Compose passes real environment variables.
API_DIR = Path(__file__).resolve().parents[2]
ROOT_ENV_FILE = API_DIR.parent.parent / ".env"


class Settings(BaseSettings):
    """Application settings, read from environment variables.

    Real environment variables take precedence over the values in the .env file.
    A missing or invalid value stops the app at startup with a clear error.
    """

    model_config = SettingsConfigDict(
        env_file=ROOT_ENV_FILE,
        # The shared .env also holds variables for other services (e.g. WEB_PORT)
        extra="ignore",
    )

    app_name: str = "API"

    postgres_user: str
    postgres_password: SecretStr
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # At least 32 characters: shorter HMAC keys can be brute-forced
    jwt_secret_key: SecretStr = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Browser origins allowed to call the API directly.
    # In .env, write it as JSON: CORS_ORIGINS=["http://localhost:3000"]
    cors_origins: list[str] = ["http://localhost:3000"]

    @property
    def database_url(self) -> str:
        # URL.create escapes special characters in the password
        url = URL.create(
            "postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )
        return url.render_as_string(hide_password=False)


@lru_cache
def get_settings() -> Settings:
    """Return the settings, read from the environment only once."""
    return Settings()
