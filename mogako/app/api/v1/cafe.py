from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from mogako.app.api.request.cafe import CafeCreateRequest
from mogako.app.api.request.vote import VoteRequest
from mogako.app.api.response.cafe import CafeResponse
from mogako.app.dto.cafe import CafeCreateDTO
from mogako.app.dto.vote import VoteDTO
from mogako.app.entity.cafe import Cafe

from mogako.app.repository.cafe import CafeRepository
from mogako.app.service.cafe import CafeService
from mogako.db.database import SessionLocal

cafe_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cafe_router.post("", response_model=CafeResponse)
def creat_cafe(request: CafeCreateRequest, db: Session = Depends(get_db)):
    service = CafeService(repo=CafeRepository(db=db))
    cafe: Cafe = service.create_cafe(dto=CafeCreateDTO(**request.dict()))
    return CafeResponse(**cafe.dict(exclude={"id"}))


@cafe_router.post("/{cafe_external_key}/vote", response_model=CafeResponse)
def vote_cafe(
    request: VoteRequest, cafe_external_key: str, db: Session = Depends(get_db)
):
    service = CafeService(repo=CafeRepository(db=db))
    cafe: Cafe = service.vote(
        dto=VoteDTO(
            cafe_external_key=cafe_external_key,
            is_like=request.is_like,
            user_id=request.user_id,
        )
    )
    return CafeResponse(**cafe.dict(exclude={"id"}))
