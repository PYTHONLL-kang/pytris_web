from uuid import UUID
from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    refresh_token: str

class Token_user(BaseModel):
    nickname : str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None