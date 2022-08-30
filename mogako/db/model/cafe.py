from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime

from mogako.db.database import Base


class Cafe(Base):
    __tablename__ = "cafe"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    naver_map_url = Column(String(64))
    opened_at = Column(DateTime)
    closed_at = Column(DateTime)
    tel = Column(String(32))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
