from sqlalchemy.orm import Session

from mogako.app.entity.cafe import Cafe
from mogako.db.model.cafe import Cafe as CafeORM


class CafeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_cafe(self, cafe: Cafe):
        cafe_orm = CafeORM(**cafe.dict())
        self.db.add(cafe_orm)
        self.db.commit()
        self.db.refresh(cafe_orm)
        cafe.cafe_id = cafe_orm.cafe_id
        return cafe
