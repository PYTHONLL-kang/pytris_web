from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form

from starlette.responses import FileResponse, RedirectResponse
from starlette import status

from sqlalchemy.orm import Session
from typing import Annotated

import jwt

from datetime import datetime, timedelta

from db.database import get_db
from db.crud import user_crud
from db.scheme import user_scheme
from db.scheme import token_scheme
from utility import tokens

router = APIRouter(
    prefix="/api/user",
)


async def get_current_user(token: str = Depends(tokens.oauth2_scheme), db: Session = Depends(get_db)):
    exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="존재하지 않는 사용자입니다")
    try:
        payload = jwt.decode(token, tokens.JWT_KEY['access'], algorithms=[tokens.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise exception
        token_data = token_scheme.Token_user(nickname=username)
    except jwt.PyJWTError:
        raise exception

    user = user_crud.search_user(db, token_data.username)
    if user is None:
        raise exception

    return user

async def get_current_user(token: str = Depends(tokens.oauth2_scheme), db: Session = Depends(get_db)):
    exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="존재하지 않는 사용자입니다")
    try:
        payload = jwt.decode(token, tokens.JWT_KEY['access'], algorithms=[tokens.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise exception
        token_data = token_scheme.Token_user(nickname=username)
    except jwt.PyJWTError:
        raise exception

    user = user_crud.search_user(db, token_data.username)
    if user is None:
        raise exception
    return user

@router.post('/register/', status_code=status.HTTP_204_NO_CONTENT)
async def create_user(nickname: str = Form(...), email: str = Form(...), nation: str = Form(...), password: str = Form(...), check_password: str = Form(...), db : Session = Depends(get_db)):
    _user_create = {'nickname' : nickname, 'email' : email, 'nation' : nation, 'password' : password, 'check_password' : check_password}
    user = user_crud.search_user(db, _user_create['nickname'])
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다")

    user_crud.create_user(db=db, user_create=_user_create)

    return RedirectResponse(url='/f/l', status_code=status.HTTP_302_FOUND)

@router.post('/login/', response_model=token_scheme.Token)
async def login(nickname: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    _user_login = {'nickname' : nickname, 'password' : password}
    user = user_crud.search_user(db, _user_login['nickname'])
    print(user.nickname)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="사용자가 존재하지 않습니다")

    if not user_crud.verify_passwrod(_user_login['password'], user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="비밀번호가 일치하지 않습니다")

    token =  {
        "access_token" : tokens.create_token(user.nickname, 'access'),
        "refresh_token" : tokens.create_token(user.nickname, 'refresh')
    }

    return token

@router.post('/token', response_model=token_scheme.Token_user)
async def read_token_user(user : token_scheme.Token_user = Depends(get_current_user)):
    return user

@router.get('/search/{username}')
async def search_user(username, db : Session = Depends(get_db)):
    user = user_crud.search_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="사용자가 존재하지 않습니다")

