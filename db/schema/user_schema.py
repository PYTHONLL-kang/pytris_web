from pydantic import BaseModel, validator
from datetime import datetime
from modules import send_email

from fastapi import Form

class UserCreate(BaseModel):
    nickname: str
    nation: str
    email: str
    password: str
    check_password: str

    # @validator('nickname', 'nation', 'email', 'password', 'check_password')
    # def not_empty(cls, v):
    #     if not v or not v.strip():
    #         raise ValueError('빈 값은 허용되지 않습니다')

    #     return v

    # @validator('nickname')
    # def valid_nickname(nickname):
    #     if len(nickname) > 10:
    #         raise ValueError('닉네임은 10글자를 넘기면 안 됩니다')

    #     return nickname

    # @validator('email')
    # def valid_email(email):
    #     if send_email(email):
    #         raise ValueError('존재하지 않는 이메일입니다')
        
    #     return email

    # @validator('password')
    # def must_equal(cls, v, values):
    #     if 'password' in values and v != values['check_passwod']:
    #         raise ValueError('비밀번호가 일치하지 않습니다')

    #     return v

class User(BaseModel):
    identifier : int
    nickname : str
    password : str
    nation : str
    email : str
    register_day : datetime

    class Config:
        orm_mode = True