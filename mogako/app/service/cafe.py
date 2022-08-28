from mogako.app.dto.cafe import CafeCreateDTO
from mogako.app.entity.cafe import Cafe
from mogako.app.repository.cafe import CafeRepository


class CafeService:
    def __init__(self, repo: CafeRepository):
        self._repo = repo

    def create_cafe(self, dto: CafeCreateDTO) -> Cafe:
        cafe = Cafe(**dto.dict())
        self._repo.create_cafe(cafe=cafe)
        return cafe
