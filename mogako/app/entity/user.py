from pydantic import BaseModel


class User(BaseModel):
    login_id: str
    password: str
    is_staff: bool = False
    user_id: int | None = None
    nickname: str | None = None


class AdminAuthorization(BaseModel):
    ...
