from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette import status

from db.database import get_db
from db.schema import user_schema
from db.crud import user_crud
from fastapi import Form

from modules.server import origins

router = APIRouter(
    prefix="/api/user",
)

def create_user(_user_create : user_schema.UserCreate, db : Session):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다")

    
    user_crud.create_user(db=db, user_create=_user_create)

@router.post('/create', status_code=status.HTTP_204_NO_CONTENT)
async def read_user(nickname: str = Form(...), email: str = Form(...), nation: str = Form(...), password: str = Form(...), check_password: str = Form(...), db : Session = Depends(get_db)):
    user = {'nickname' : nickname, 'email' : email, 'nation' : nation, 'password' : password, 'check_password' : check_password}

    create_user(user, db)

@router.get('/search/{username}')
async def search_user(username, db : Session = Depends(get_db)):
    user_crud.search_user(db, username)