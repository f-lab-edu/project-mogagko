from sqlalchemy.orm import Session

from mogako.app.entity.cafe import Cafe, Comment
from mogako.app.entity.vote import Vote
from mogako.db.model.cafe import Cafe as CafeORM, Vote as VoteORM, Comment as CommentORM


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

    def extract_cafe_id(self, external_key):
        cafe_id = (
            self.db.query(CafeORM)
            .filter(CafeORM.external_key == external_key)
            .first()
            .cafe_id
        )
        return cafe_id

    def update_cafe(self, cafe: Cafe, external_key):
        self.db.query(CafeORM).filter(CafeORM.external_key == external_key).update(
            cafe.dict()
        )
        self.db.commit()
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
        self._update_cafe_count_like(cafe_id=cafe_id, is_like=is_like)
        self.db.commit()
        self.db.refresh(vote_orm)
        return Vote(
            cafe_id=vote_orm.cafe_id,
            user_id=vote_orm.user_id,
            is_like=vote_orm.is_like,
        )

    def _update_cafe_count_like(self, cafe_id: int, is_like: bool):
        q = self.db.query(VoteORM).filter_by(cafe_id=cafe_id, is_like=True)
        total_count_like = q.count()
        self.db.query(CafeORM).filter(CafeORM.cafe_id == cafe_id).update(
            {"count_like": total_count_like}
        )

    def update_vote(self, vote: Vote):
        self.db.query(VoteORM).filter_by(
            cafe_id=vote.cafe_id, user_id=vote.user_id
        ).update({"is_like": vote.is_like})
        self._update_cafe_count_like(cafe_id=vote.cafe_id, is_like=vote.is_like)
        cafe_orm = self.db.query(CafeORM).filter_by(cafe_id=vote.cafe_id).first()
        self.db.commit()
        return Cafe(**cafe_orm.dict())


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, comment: Comment, cafe_external_key):
        cafe_orm = (
            self.db.query(CafeORM)
            .filter(CafeORM.external_key == cafe_external_key)
            .first()
        )
        comment_orm = CommentORM(**comment.dict(), cafe_id=cafe_orm.cafe_id)
        self.db.add(comment_orm)
        self.db.commit()
        self.db.refresh(comment_orm)
        return comment
