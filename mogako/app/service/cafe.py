from mogako.app.dto.cafe import (
    CafeCreateDTO,
    CafeUpdateDTO,
    CommentCreateDTO,
    CafeReadDTO,
    CafeSearchDTO,
)
from mogako.app.dto.vote import VoteDTO
from mogako.app.entity.cafe import Cafe, Comment
from mogako.app.repository.cafe import CafeRepository, CommentRepository


class CafeService:
    def __init__(self, repo: CafeRepository):
        self._repo = repo

    def create_cafe(self, dto: CafeCreateDTO) -> Cafe:
        cafe = Cafe(**dto.dict())
        self._repo.create_cafe(cafe=cafe)
        return cafe

    def get_cafe(self, dto: CafeReadDTO) -> Cafe:
        cafe = self._repo.get_cafe(**dto.dict())
        return cafe

    def search_cafe(self, dto: CafeSearchDTO) -> Cafe:
        cafe = self._repo.search_cafe(**dto.dict())
        return cafe

    def update_cafe(self, dto: CafeUpdateDTO, external_key):
        cafe_id = self._repo.extract_cafe_id(external_key)
        cafe = Cafe(**dto.dict(), cafe_id=cafe_id)
        self._repo.update_cafe(cafe=cafe, external_key=external_key)
        return cafe

    def vote(self, dto: VoteDTO) -> Cafe:
        cafe = self._repo.get_cafe(external_key=dto.cafe_external_key)
        vote = self._repo.get_vote(cafe_id=cafe.cafe_id, user_id=dto.user_id)
        if vote is None:
            vote = self._repo.create_vote(
                cafe_id=cafe.cafe_id, user_id=dto.user_id, is_like=dto.is_like
            )
            cafe = self._repo.get_cafe(external_key=dto.cafe_external_key)

        elif vote.is_like != dto.is_like:
            vote.is_like = dto.is_like
            cafe = self._repo.update_vote(vote=vote)

        return cafe


class CommentService:
    def __init__(self, repo: CommentRepository):
        self._repo = repo

    def create_comment(self, dto: CommentCreateDTO, cafe_external_key):
        comment = Comment(**dto.dict())
        self._repo.create_comment(comment=comment, cafe_external_key=cafe_external_key)
        return comment
