from fastapi import FastAPI, Query, Form

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from typing import Annotated, Optional

from db.router import user_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5000", # pyg
    "http://localhost:5500", # front
    "http://localhost:8000", # back
]

app.include_router(user_router.router)

@app.get("/")
async def root():
    return {'2317' : "이강"}

@app.get("/f", response_class=RedirectResponse)
async def front_response():
    return 'http://127.0.0.1:5500/frontend/html/main.html'

@app.get("/ping/{pong}")
async def test(pong):
    return {"message" : pong}