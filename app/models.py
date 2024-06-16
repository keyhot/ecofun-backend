from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class UserScore(Base):
    __tablename__ = "posts"

    id = Column(String,primary_key=True,nullable=False)
    score = Column(Integer,nullable=False, server_default=text('0'))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class MarketplaceUnit(Base):
    __tablename__ = "marketplaces"

    id = Column(Integer,primary_key=True,nullable=False)
    image = Column(String,nullable=False)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    price = Column(Integer,nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}