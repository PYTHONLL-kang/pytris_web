from fastapi import FastAPI, Query, Form

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from typing import Annotated, Optional

from db.database import engine
from db.data_schema import User

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # front
    "http://localhost:8000",  # back
]

@app.get("/")
async def root():
    return {'2317' : "이강"}

@app.get("/f", response_class=RedirectResponse)
async def front_response():
    return 'http://127.0.0.1:5500/frontend/html/main.html'

@app.get("/ping/{pong}")
async def test(pong):
    return {"message" : pong}

@app.post("/users/")
async def create_user(nickname: str = Form(...), nation: str = Form(...), email: str = Form(...), password: str = Form(...)):

    if len(nickname) > 10:
        return
    user = User.parse_obj({"nickname" : nickname, "nation" : nation, "email" : email, "password" : password})
    return user

@app.post("/login/")
async def validate_user(user : User):
    pass