from datetime import datetime

from sqlalchemy.orm import Session

from db.schema.user_schema import UserCreate
from models.User import User

def create_user(db : Session, user_create : UserCreate):
    db_user = User(
                    nickname=user_create.nickname,
                    password=user_create.password,
                    nation=user_create.nation,
                    email=user_create.email,
                    register_day=datetime.now
                    )
    
    db.add(db_user)
    db.commit()

def get_existing_user(db : Session, user_create : UserCreate):
    return db.query(User).filter(
        (User.nickname == user_create['nickname']) |
        (User.email == ['user_create.email'])
    )