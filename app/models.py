from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class UserScore(Base):
    __tablename__ = "posts"

    id = Column(String,primary_key=True,nullable=False)
    score = Column(Integer,nullable=False, server_default=text('0'))

class MarketplaceUnit(Base):
    __tablename__ = "marketplaces"

    id = Column(Integer,primary_key=True,nullable=False)
    image = Column(String,nullable=False)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    price = Column(Integer,nullable=False)