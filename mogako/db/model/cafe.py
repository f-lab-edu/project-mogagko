from sqlalchemy import Boolean, Column, Integer
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from mogako.db.database import Base


class DBModelUtil:
    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Cafe(Base, DBModelUtil):
    __tablename__ = "cafe"

    cafe_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    external_key = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    address = Column(String(258))
    description = Column(String(512))
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String(64))
    state = Column(String(64))
    remaining_address = Column(String(128))
    postcode = Column(String(64))
    surrounding_station = Column(String(64))
    is_parking = Column(Boolean)
    naver_map_url = Column(String(512))
    tel = Column(String(32))
    count_like = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    opening_days = relationship("OpeningDay", back_populates="cafe")
    cafe_tags = relationship("CafeTag", back_populates="cafe")
    images = relationship("Image", back_populates="cafe")
    votes = relationship("Vote", back_populates="cafe")

    comments = relationship("Comment", back_populates="cafe")


class OpeningDay(Base, DBModelUtil):
    __tablename__ = "opening_day"

    opening_day_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    week = Column(String(32))

    # TINYINT로 추후에 데이터 타입 수정
    start_time_hour = Column(Integer)
    start_time_miniute = Column(Integer)
    end_time_hour = Column(Integer)
    end_time_miniute = Column(Integer)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="opening_days")


class CafeTag(Base, DBModelUtil):
    __tablename__ = "cafe_tag"

    cafe_tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="cafe_tags")

    tag = relationship("Tag", back_populates="cafe_tags")


class Tag(Base, DBModelUtil):
    __tablename__ = "tag"

    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cafe_tag_id = Column(Integer, ForeignKey("cafe_tag.cafe_tag_id"))

    tag = Column(String(128))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe_tags = relationship("CafeTag", back_populates="tag")


class Image(Base, DBModelUtil):
    __tablename__ = "image"

    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))

    is_represenative = Column(Boolean)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="images")


class Vote(Base, DBModelUtil):
    __tablename__ = "vote"

    vote_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    is_like = Column(Boolean)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="votes")
    user = relationship("User", back_populates="votes")


class Comment(Base, DBModelUtil):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    external_key = Column(String(50), unique=True, index=True, nullable=False)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    comment = Column(String(512))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="comments")


class User(Base, DBModelUtil):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    votes = relationship("Vote", back_populates="user")
