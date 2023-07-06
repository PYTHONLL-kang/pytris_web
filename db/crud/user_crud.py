import datetime

from sqlalchemy.orm import Session

from passlib.context import CryptContext

from db.scheme.user_scheme import UserCreate
from models.User import User

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_passwrod(password: str) -> str:
    return password_context.hash(password)

def verify_passwrod(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_user(db: Session, user_create: UserCreate):
    db_user = User(
                    nickname=user_create['nickname'],
                    email=user_create['email'],
                    nation=user_create['nation'],
                    password=get_hashed_passwrod(user_create['password']),
                    registe_day=datetime.datetime.now()
                    )
    
    db.add(db_user)
    db.commit()

def search_user(db: Session, username: str):
    return db.query(User).filter((User.nickname == username)).first()
