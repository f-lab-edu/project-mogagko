from pydantic import BaseModel


class UserTokenDTO(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserSignUpDTO(BaseModel):
    login_id: str
    password: str
    nickname: str | None = None
