from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class User(Base):
    __table_name__ = "users"

    identifier = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    nation = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
