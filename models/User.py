from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class User(Base):
    __tablename__ = "users"

    identifier = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    nation = Column(String, unique=False, nullable=False)
    password = Column(String, unique=False, nullable=False)
    registe_day = Column(DateTime, unique=False, nullable=False)

    def __init__(self, nickname, email, nation, password, registe_day):
        self.nickname = nickname
        self.email = email
        self.nation = nation
        self.password = password
        self.register_day = registe_day
        
