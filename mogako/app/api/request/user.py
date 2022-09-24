from pydantic import BaseModel


class UserSignUp(BaseModel):
    login_id: str
    password: str
    nickname: str | None = None
