from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class User(Base):
    __tablename__ = "users"

    identifier = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=False, nullable=False)
    nation = Column(String, unique=False, nullable=False)
    registe_day = Column(DateTime, unique=False, nullable=False)

    def __init__(self, identifier, nickname, password, nation, email, registe_day):
        self.identifier = identifier
        self.nickname = nickname
        self.password = password
        self.nation = nation
        self.email = email
        self.register_day = registe_day
        
