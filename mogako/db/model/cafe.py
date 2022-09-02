from sqlalchemy import Boolean, Column, Integer
from sqlalchemy import String, Float, DateTime, ForeignKey

from sqlalchemy.orm import relationship
from mogako.db.database import Base


class Cafe(Base):
    __tablename__ = "cafe"

    cafe_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    external_key = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    address = Column(String(258))
    description = Column(String)
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

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    opening_day = relationship("OpeningDay", back_populates="opening_day")
    cafe_tag = relationship("CafeTag", back_populates="cafe_tag")
    image = relationship("Image", back_populates="image")
    vote = relationship("Vote", back_populates="vote")

    comment = relationship("Comment", back_populates="comment")


class OpeningDay(Base):
    __tablename__ = "opening_day"

    cafe_opening_day_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )

    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    week = Column(String(32))

    # TINYINT로 추후에 데이터 타입 수정
    start_time_hour = Column(Integer)
    start_time_miniute = Column(Integer)
    end_time_hour = Column(Integer)
    end_time_miniute = Column(Integer)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="opening_day")


class CafeTag(Base):
    __tablename__ = "cafe_tag"

    cafe_tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="cafe_tag")

    tag = relationship("Tag", back_populates="cafe_tag")


class Tag(Base):
    __tablename__ = "tag"

    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cafe_tag_id = Column(Integer, ForeignKey("cafe_tag.cafe_tag_id"))

    tag = Column(String(128))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe_tag = relationship("CafeTag", back_populates="tag")


class Image(Base):
    __tablename__ = "image"

    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))

    is_represenative = Column(Boolean)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="image")


class Vote(Base):
    __tablename__ = "vote"

    vote_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))

    is_like = Column(Boolean)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="vote")


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    comment = Column(String)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe = relationship("Cafe", back_populates="comment")
