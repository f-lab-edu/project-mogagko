from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from mogako.app.api.request.cafe import (
    CafeCreateRequest,
    CafeUpdateRequest,
    CommentCreateRequest,
)
from mogako.app.api.request.vote import VoteRequest
from mogako.app.api.response.cafe import (
    CafeResponse,
    CafeUpdateResponse,
    CommentCreateResponse,
)
from mogako.app.dto.cafe import CafeCreateDTO, CafeUpdateDTO, CommentCreateDTO
from mogako.app.dto.vote import VoteDTO
from mogako.app.entity.cafe import Cafe, Comment

from mogako.app.repository.cafe import CafeRepository, CommentRepository
from mogako.app.service.cafe import CafeService, CommentService
from mogako.db.database import db

cafe_router = APIRouter()


@cafe_router.post("", response_model=CafeResponse)
def creat_cafe(request: CafeCreateRequest, db: Session = Depends(db.session)):
    service = CafeService(repo=CafeRepository(db=db))
    cafe: Cafe = service.create_cafe(dto=CafeCreateDTO(**request.dict()))
    return CafeResponse(**cafe.dict(exclude={"id"}))


@cafe_router.post("/{cafe_external_key}/vote", response_model=CafeResponse)
def vote_cafe(
    request: VoteRequest, cafe_external_key: str, db: Session = Depends(db.session)
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


@cafe_router.patch("/{external_key}", response_model=CafeResponse)
def update_cafe(
    external_key: str, request: CafeUpdateRequest, db: Session = Depends(db.session)
):
    service = CafeService(repo=CafeRepository(db=db))
    cafe: Cafe = service.update_cafe(
        dto=CafeUpdateDTO(**request.dict()), external_key=external_key
    )
    return CafeUpdateResponse(**cafe.dict())


@cafe_router.post("/{cafe_external_key}/comment", response_model=CommentCreateResponse)
def create_comment(
    cafe_external_key: str,
    request: CommentCreateRequest,
    db: Session = Depends(db.session),
):
    service = CommentService(repo=CommentRepository(db=db))
    comment: Comment = service.create_comment(
        dto=CommentCreateDTO(**request.dict()), cafe_external_key=cafe_external_key
    )
    return CommentCreateResponse(**comment.dict(), cafe_external_key=cafe_external_key)
