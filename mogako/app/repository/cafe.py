from sqlalchemy.orm import Session

from mogako.app.entity.cafe import Cafe
from mogako.app.entity.vote import Vote
from mogako.db.model.cafe import Cafe as CafeORM, Vote as VoteORM


class CafeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_cafe(self, cafe: Cafe) -> Cafe:
        cafe_orm = CafeORM(**cafe.dict())
        self.db.add(cafe_orm)
        self.db.commit()
        self.db.refresh(cafe_orm)
        cafe.cafe_id = cafe_orm.cafe_id
        return cafe

    def get_cafe(self, external_key: str) -> Cafe:
        cafe_orm = self.db.query(CafeORM).filter_by(external_key=external_key).first()
        cafe = Cafe(**cafe_orm.dict())
        return cafe

    def get_vote(self, cafe_id: int, user_id: int) -> Vote | None:
        vote_orm = (
            self.db.query(VoteORM).filter_by(cafe_id=cafe_id, user_id=user_id).first()
        )
        if vote_orm is None:
            return None
        return Vote(
            cafe_id=vote_orm.cafe_id,
            user_id=vote_orm.user_id,
            is_like=vote_orm.is_like,
        )

    def create_vote(self, cafe_id: int, user_id: int, is_like: bool) -> Vote:
        vote_orm = VoteORM(cafe_id=cafe_id, user_id=user_id, is_like=is_like)
        self.db.add(vote_orm)
        self.db.commit()
        self.db.refresh(vote_orm)
        return Vote(
            cafe_id=vote_orm.cafe_id,
            user_id=vote_orm.user_id,
            is_like=vote_orm.is_like,
        )

    def update_vote(self, vote: Vote):
        self.db.query(VoteORM).filter_by(
            cafe_id=vote.cafe_id, user_id=vote.user_id
        ).update({"is_like": vote.is_like})
        self.db.query(CafeORM).filter_by(cafe_id=vote.cafe_id).update(
            {
                "count_like": CafeORM.count_like + 1
                if vote.is_like
                else CafeORM.count_like - 1
            }
        )
        cafe_orm = self.db.query(CafeORM).filter_by(cafe_id=vote.cafe_id).first()
        self.db.commit()
        return Cafe(**cafe_orm.dict())
