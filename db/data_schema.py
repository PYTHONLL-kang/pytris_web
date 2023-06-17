import datetime

from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    identifier = int
    nickname: str
    nation : str
    email: EmailStr
    password: str
    password_check: str
    register_day : datetime.datetime

    @validator('nickname', 'nation', 'email', 'password', 'password_check')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('password_check')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True