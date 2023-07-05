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

@router.post('/register/', status_code=status.HTTP_204_NO_CONTENT)
async def read_user(nickname: str = Form(...), email: str = Form(...), nation: str = Form(...), password: str = Form(...), check_password: str = Form(...), db : Session = Depends(get_db)):
    _user_create = {'nickname' : nickname, 'email' : email, 'nation' : nation, 'password' : password, 'check_password' : check_password}
    user = user_crud.search_user(db, _user_create['nickname'])
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다")

    user_crud.create_user(db=db, user_create=_user_create)

    return RedirectResponse(url='/f/l', status_code=status.HTTP_302_FOUND)

@router.post('/login/', status_code=status.HTTP_204_NO_CONTENT)
async def read_transit(nickname: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    _user_login = {'nickname' : nickname, 'password' : password}
    user = user_crud.search_user(db, _user_login['nickname'])

    if user.password != _user_login['password']:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="비밀번호가 일치하지 않습니다")

    return RedirectResponse(url='/f/{0}'.format(nickname), status_code=status.HTTP_302_FOUND)

@router.get('/search/{username}')
async def search_user(username, db : Session = Depends(get_db)):
    user = user_crud.search_user(db, username)
    if user:
        return user