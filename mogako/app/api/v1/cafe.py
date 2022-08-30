from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from mogako.app.api.request.cafe import CafeCreateRequest
from mogako.app.api.response.cafe import CafeCreateResponse
from mogako.app.dto.cafe import CafeCreateDTO
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


@cafe_router.post("", response_model=CafeCreateResponse)
def creat_cafe(request: CafeCreateRequest, db: Session = Depends(get_db)):
    service = CafeService(repo=CafeRepository(db=db))
    cafe: Cafe = service.create_cafe(dto=CafeCreateDTO(**request.dict()))
    return CafeCreateResponse(**cafe.dict(exclude={"id"}))
