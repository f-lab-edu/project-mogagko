from datetime import datetime

from pydantic import BaseModel


class CafeResponse(BaseModel):
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
    count_like: int | None
    created_at: datetime
    updated_at: datetime


class CafeUpdateResponse(BaseModel):
    external_key: str | None
    name: str | None
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
    created_at: datetime
    updated_at: datetime


class CommentCreateResponse(BaseModel):
    external_key: str
    comment: str
    cafe_external_key: str
    created_at: datetime
    updated_at: datetime
