from pydantic import BaseModel


class CafeCreateDTO(BaseModel):
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


class CafeReadDTO(BaseModel):
    external_key: str


class CafeUpdateDTO(BaseModel):
    name: str | None = None
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


class CommentCreateDTO(BaseModel):
    comment: str
