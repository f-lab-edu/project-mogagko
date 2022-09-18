from pydantic import BaseModel


class UserTokenResponse(BaseModel):
    Authorization: str
