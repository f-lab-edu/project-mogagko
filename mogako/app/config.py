"""
get_settings gets called for each request.
 lru_cache to cache the settings so get_settings is only called once.
lru_cache
https://docs.python.org/3/library/functools.html#functools.lru_cache

"""
import logging
from os import path, environ
from dataclasses import dataclass


log = logging.getLogger("uvicorn")

base_dir = path.dirname(path.dirname(path.abspath(__file__)))


@dataclass
class Config:
    BASE_DIR = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True
    DB_URL: str = "sqlite:///./sql_app.db"


@dataclass
class DevConfig(Config):
    PROJ_RELOAD: bool = False
    DB_URL: str = "mysql+pymysql://db_manager:dpvmfoq1A@db-bj72i.pub-cdb.ntruss.com/mogagko-db?charset=utf8mb4"


def conf():
    config = dict(dev=DevConfig(), local=LocalConfig())
    return config.get(environ.get("ENVIRONMENT", "local"))
