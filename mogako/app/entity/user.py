from pydantic import BaseModel


class User(BaseModel):
    login_id: str
    password: str
    user_id: int | None = None
    nickname: str | None = None


class AdminAuthorization(BaseModel):
    ...
