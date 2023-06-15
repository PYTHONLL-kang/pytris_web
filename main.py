from fastapi import FastAPI, Query, Form
from typing import Annotated, Optional
from pydantic import BaseModel
import json

class User(BaseModel):
    nickname : str
    nation : str
    email : str
    password : str
    unique_id : int

app = FastAPI()
ID = 0

@app.get("/")
async def root():
    return {'2317' : "이강"}

@app.get("/ping/{pong}")
async def test(pong):
    return {"message" : pong}

@app.post("/users/")
async def create_user(nickname: str = Form(...), nation: str = Form(...), email: str = Form(...), password: str = Form(...)):

    if len(nickname) > 10:
        return
    user = User.parse_obj({"nickname" : nickname, "nation" : nation, "email" : email, "password" : password, "unique_id" : ID})
    ID += 1
    return user

@app.post("/login/")
async def validate_user(user : User):
    pass