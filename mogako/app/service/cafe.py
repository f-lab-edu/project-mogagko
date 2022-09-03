from mogako.app.dto.cafe import CafeCreateDTO
from mogako.app.dto.vote import VoteDTO
from mogako.app.entity.cafe import Cafe
from mogako.app.repository.cafe import CafeRepository


class CafeService:
    def __init__(self, repo: CafeRepository):
        self._repo = repo

    def create_cafe(self, dto: CafeCreateDTO) -> Cafe:
        cafe = Cafe(**dto.dict())
        self._repo.create_cafe(cafe=cafe)
        return cafe

    def vote(self, dto: VoteDTO) -> Cafe:
        cafe = self._repo.get_cafe(external_key=dto.cafe_external_key)
        vote = self._repo.get_vote(cafe_id=cafe.cafe_id, user_id=dto.user_id)
        if vote is None:
            vote = self._repo.create_vote(
                cafe_id=cafe.cafe_id, user_id=dto.user_id, is_like=dto.is_like
            )

        if vote.is_like != dto.is_like:
            vote.is_like = dto.is_like
            cafe = self._repo.update_vote(vote=vote)
        return cafe
