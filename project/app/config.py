import logging
import os
from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.environ.get("DATABASE_URL")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from env")
    return Settings()
