from sqlalchemy.orm import Session

from mogako.app.entity.user import User
from mogako.db.model.cafe import User as UserORM


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_login_id(self, login_id: str) -> str | None:
        user_orm = self.db.query(UserORM).filter_by(login_id=login_id).first()
        if user_orm:
            return user_orm.login_id
        return None

    def create_user(self, user: User) -> User:
        user_orm = UserORM(
            login_id=user.login_id, password=user.password, nickname=user.nickname
        )
        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        user.user_id = user_orm.user_id
        return user

    def get_user(self, login_id: str) -> User | None:
        user_orm = self.db.query(UserORM).filter_by(login_id=login_id).first()
        if user_orm:
            return User(
                user_id=user_orm.user_id,
                login_id=user_orm.login_id,
                password=user_orm.password,
                nickname=user_orm.nickname,
                is_staff=user_orm.is_staff,
            )
        return None
