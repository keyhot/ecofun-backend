import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from .constants import DATABASE_URL
from sqlalchemy import Table, Column, MetaData, Integer, Computed

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

metadata = MetaData()

def get_db():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

data = Table(
    "users",
    metadata,
    Column('id', String, primary_key=True),
    Column('score', Integer)
)

data2 = Table(
    "marketplaces",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('image', String),
    Column('title', String),
    Column('description', String),
    Column('price', Integer),
)

Session = sessionmaker(bind=engine)