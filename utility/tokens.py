from fastapi.security import OAuth2PasswordBearer
from starlette.config import Config

import jwt

from datetime import datetime, timedelta
from typing import Union, Any

from db.scheme import user_scheme
from db.scheme import token_scheme
from utility import tokens

ALGORITHM = "HS256"

config = Config('.env')
TOKEN_EXPIRE_MINUTES = {'access' : 60*5, 'refresh' : 60*24*7}
JWT_KEY = {'access' : config('JWT_SECRET_KEY'), 'refresh' : config('JWT_REFRESH_SECRET_KEY')}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(subject: Union[str, Any], token_type: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES[token_type])

    to_encode = {'exp' : expires_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_KEY[token_type], ALGORITHM)
    return encoded_jwt
