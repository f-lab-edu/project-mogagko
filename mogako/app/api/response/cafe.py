from datetime import datetime

from pydantic import BaseModel


class CafeCreateResponse(BaseModel):
    external_key: str
    name: str
    address: str | None
    description: str | None
    latitude: float | None
    longitude: float | None
    city: str | None
    state: str | None
    remaining_address: str | None
    postcode: str | None
    surrounding_station: str | None
    is_parking: bool | None
    naver_map_url: str | None
    tel: str | None
    opened_at: datetime | None
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime
