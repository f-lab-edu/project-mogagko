from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from mogako.app.api.request.user import UserSignUp
from mogako.app.api.response.user import UserTokenResponse
from mogako.app.dto.user import UserTokenDTO, UserSignUpDTO
from mogako.app.repository.user import UserRepository
from mogako.app.service.user import UserService

from mogako.db.database import db

user_router = APIRouter()


@user_router.post("", response_model=UserTokenResponse)
def sign_up(request: UserSignUp, db: Session = Depends(db.session)):
    service = UserService(repo=UserRepository(db=db))
    login_id = service.get_login_id(login_id=request.login_id)
    if login_id:
        return JSONResponse(status_code=400, content={"message": "생성할 수 없는 아이디 입니다."})
    token: UserTokenDTO = service.sign_up(dto=UserSignUpDTO(**request.dict()))
    return UserTokenResponse(Authorization=f"{token.token_type} {token.access_token}")


@user_router.post("/login", response_model=UserTokenResponse)
def login(request: UserSignUp, db: Session = Depends(db.session)):
    service = UserService(repo=UserRepository(db=db))
    login_id = service.get_login_id(login_id=request.login_id)
    if not login_id:
        return JSONResponse(status_code=400, content={"message": "로그인 정보가 올바르지 않습니다."})
    token: UserTokenDTO = service.login(dto=UserSignUpDTO(**request.dict()))
    return UserTokenResponse(Authorization=f"{token.token_type} {token.access_token}")
