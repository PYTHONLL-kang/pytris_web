import datetime

from sqlalchemy.orm import Session

from db.schema.user_schema import UserCreate
from models.User import User

def create_user(db : Session, user_create : UserCreate):
    db_user = User(
                    nickname=user_create['nickname'],
                    email=user_create['email'],
                    nation=user_create['nation'],
                    password=user_create['password'],
                    registe_day=datetime.datetime.now()
                    )
    
    db.add(db_user)
    db.commit()

def search_user(db : Session, username : str):
    return db.query(User).filter((User.nickname == username)).first()
