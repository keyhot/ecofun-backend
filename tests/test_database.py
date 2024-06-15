# test_database.py

import pytest
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from app.constants import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    isolation_level="REPEATABLE READ"
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column('id', String, primary_key=True),
    Column('score', Integer)
)

Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)

def test_insert_and_query(setup_database):
    session = Session()
    session.execute(users.insert().values(id='user1', score=100))
    result = session.query(users).filter_by(id='user1').first()
    assert result.score == 100
    session.close()

