from pydantic import BaseModel


class VoteRequest(BaseModel):
    is_like: bool
    user_id: int
