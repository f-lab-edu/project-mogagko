import uuid
from datetime import datetime

from pydantic import BaseModel, Field


def generate_external_key():
    return str(uuid.uuid4())


class Cafe(BaseModel):
    id: int | None = None
    external_key: str = Field(default_factory=generate_external_key)
    name: str
    address: str | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    city: str | None = None
    state: str | None = None
    remaining_address: str | None = None
    postcode: str | None = None
    surrounding_station: str | None = None
    is_parking: bool | None = None
    naver_map_url: str | None = None
    tel: str | None = None
    opened_at: datetime | None = None
    closed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
