from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from starlette.config import Config

config = Config('.env')

SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()