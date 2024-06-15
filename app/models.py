from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class UserScore(Base):
    __tablename__ = "posts"

    id = Column(String,primary_key=True,nullable=False)
    score = Column(Integer,nullable=False, server_default=text('0'))