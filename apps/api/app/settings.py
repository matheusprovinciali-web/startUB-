from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_env: str = 'development'
    database_url: str | None = None
    auth_issuer: str | None = None
    auth_client_id: str | None = None
    auth_audience: str | None = None
    auth_jwks_url: str | None = None
    cors_origins: list[str] = []
    db_pool_min_size: int = 1
    db_pool_max_size: int = 10

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(',') if item.strip()]
        return value

    @property
    def auth_configured(self) -> bool:
        return bool(self.auth_issuer and self.auth_client_id and self.auth_jwks_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
