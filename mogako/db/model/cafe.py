from sqlalchemy import Boolean, Column, Integer
from sqlalchemy import String, Float, DateTime, ForeignKey

# from sqlalchemy.dialects.mysql import TINYINT
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
    # opened_at = Column(DateTime)
    # closed_at = Column(DateTime)
    tel = Column(String(32))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe_cafe_opening_day = relationship(
        "CafeOpeningDay", back_populates="cafe_opening_day_cafe"
    )
    cafe_cafe_x_tag = relationship("CafeXTag",\
                                   back_populates="cafe_x_tag_cafe")
    cafe_image = relationship("Image", back_populates="image_cafe")
    cafe_vote = relationship("Vote", back_populates="vote_cafe")

    cafe_comment = relationship("Comment", back_populates="comment_cafe")


class CafeOpeningDay(Base):
    __tablename__ = "cafe_opening_day"

    cafe_opening_day_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )

    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    week = Column(String(32))
    # TINYINT
    start_time_hour = Column(Integer)
    start_time_miniute = Column(Integer)
    end_time_hour = Column(Integer)
    end_time_miniute = Column(Integer)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe_opening_day_cafe = relationship("Cafe", back_populates="cafe_cafe_opening_day")


class CafeXTag(Base):
    __tablename__ = "cafe_x_tag"

    cafe_x_tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe_x_tag_cafe = relationship("Cafe", back_populates="cafe_cafe_x_tag")

    cafe_x_tag_cafe_tag = relationship("CafeTag", back_populates="cafe_tag_cafe_x_tag")


class CafeTag(Base):
    __tablename__ = "cafe_tag"

    cafe_tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    cafe_x_tag_id = Column(Integer, ForeignKey("cafe_x_tag.cafe_x_tag_id"))

    tag = Column(String(128))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    cafe_tag_cafe_x_tag = relationship("CafeXTag", back_populates="cafe_x_tag_cafe_tag")


class Image(Base):
    __tablename__ = "image"

    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))

    is_represenative = Column(Boolean)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    image_cafe = relationship("Cafe", back_populates="cafe_image")


class Vote(Base):
    __tablename__ = "vote"

    vote_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))

    # user_id = Column(Integer, ForeignKey("User.user_id"))

    is_like = Column(Boolean)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    vote_cafe = relationship("Cafe", back_populates="cafe_vote")


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    comment = Column(String)
    user_id = Column(Integer, ForeignKey("User.user_id"))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    comment_cafe = relationship("Cafe", back_populates="cafe_comment")
