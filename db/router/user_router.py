from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.database import get_db
from db.schema import user_schema
from db.crud import user_crud

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create")
def create_user(_user_create : user_schema.UserCreate, db : Session = Depends(get_db)):
    # user = user_crud.get_existing_user(db, user_create=_user_create)
    # if user:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail="이미 존재하는 사용자입니다")

    user_crud.create_user(db=db, user_create=_user_create)