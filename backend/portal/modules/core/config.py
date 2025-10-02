"""Load env"""
import os
from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends
from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Env"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OKTA_CLIENT_ID: Optional[str] = os.getenv("OKTA_CLIENT_ID")
    OKTA_DOMAIN: Optional[str] = os.getenv("OKTA_DOMAIN")

    PGUSER: str = os.getenv("PGUSER", "postgres")
    PGPASSWORD: str = os.getenv("PGPASSWORD", "postgres")
    PGDATABASE: str = os.getenv("PGDATABASE", "postgres")
    PGPORT: int = int(os.getenv("PGPORT", "5432"))
    PGHOST: str = os.getenv("PGHOST", "postgres")
    PG_URI: Optional[str] = None

    @field_validator("PG_URI")
    @classmethod
    def assemble_db_connection(cls, v: PostgresDsn, info: ValidationInfo):
        """assemble pg uri"""
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(  # type: ignore
                scheme="postgresql",
                host=info.data["PGHOST"],
                port=info.data["PGPORT"],
                username=info.data["PGUSER"],
                password=info.data["PGPASSWORD"],
                path=f"{info.data['PGDATABASE'] or info.data['PGUSER']}",
            )
        )


@lru_cache
def configs() -> Settings:
    """init setting"""
    production = os.getenv("PRODUCTION", "false") == "true"
    if production:
        return Settings(_env_file=None)  # type: ignore
    return Settings()


Env = Annotated[Settings, Depends(configs)]
