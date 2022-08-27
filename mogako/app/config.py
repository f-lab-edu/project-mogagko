"""
get_settings gets called for each request.
 lru_cache to cache the settings so get_settings is only called once.
lru_cache
https://docs.python.org/3/library/functools.html#functools.lru_cache

"""
import logging
import os
from functools import lru_cache

from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment = os.getenv("ENVIRONMENT", "dev")
    testing = os.getenv("TESTING", 0)


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
