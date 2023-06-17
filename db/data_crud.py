from datetime import datetime

from sqlalchemy.orm import Session

from data_schema import userCreate, userUpdate
from data_table import User


def create_user(db: Session, user_create: userCreate, user: User):
    db_user = User(user_create)
    db.add(db_user)
    db.commit()


def get_user(db: Session, user_id: int):
    return db.query(User).get(user_id)


def update_user(db: Session, db_user: User,
                  user_update: userUpdate):
    db_user.content = user_update.content
    db_user.modify_date = datetime.now()
    db.add(db_user)
    db.commit()


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
