"""
get_settings gets called for each request.
 lru_cache to cache the settings so get_settings is only called once.
lru_cache
https://docs.python.org/3/library/functools.html#functools.lru_cache
"""
import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

log = logging.getLogger("uvicorn")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))


@dataclass
class Config:
    BASE_DIR = BASE_DIR
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True


@dataclass
class DevConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    config = dict(dev=DevConfig(), local=LocalConfig())
    return config.get(os.getenv("ENVIRONMENT", "local"))
