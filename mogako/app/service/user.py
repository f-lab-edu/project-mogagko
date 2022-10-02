import os
from datetime import datetime, timedelta
from typing import Dict

import bcrypt
from jose import jwt
from dotenv import load_dotenv

from mogako.app.dto.user import UserTokenDTO, UserSignUpDTO
from mogako.app.entity.user import User
from mogako.app.repository.user import UserRepository

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "..", "..", ".env"))
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def get_login_id(self, login_id: str) -> str | None:
        return self._repo.get_login_id(login_id=login_id)

    def sign_up(self, dto: UserSignUpDTO) -> UserTokenDTO:
        hash_pw = bcrypt.hashpw(dto.password.encode("utf-8"), bcrypt.gensalt())
        user: User = self._repo.create_user(
            user=User(login_id=dto.login_id, password=hash_pw, nickname=dto.nickname)
        )
        return UserTokenDTO(
            access_token=self._create_access_token(data={"sub": user.login_id})
        )

    def _create_access_token(self, data: Dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def login(self, dto: UserSignUpDTO) -> UserTokenDTO:
        user = self._repo.get_user(login_id=dto.login_id)
        if not user:
            raise Exception("User not found")
        is_verified = bcrypt.checkpw(
            password=dto.password.encode("utf-8"),
            hashed_password=user.password.encode("utf-8"),
        )
        if not is_verified:
            raise Exception("User not found")
        return UserTokenDTO(
            access_token=self._create_access_token(data={"sub": user.login_id})
        )
