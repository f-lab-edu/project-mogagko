from pydantic import BaseModel


class Vote(BaseModel):
    user_id: int
    cafe_id: int
    is_like: bool
