from pydantic import BaseModel


class VoteDTO(BaseModel):
    cafe_external_key: str
    is_like: bool
    user_id: int
