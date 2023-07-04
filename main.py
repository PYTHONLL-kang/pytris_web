from fastapi import FastAPI, Query, Form

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from typing import Annotated, Optional

from db.router import user_router
from modules.server import origins

app = FastAPI()

app.include_router(user_router.router)

@app.get("/")
async def root():
    return {'2317' : "이강"}

@app.post("/f", response_class=RedirectResponse)
async def front_response():
    return origins['front'] + '/frontend/html/main.html'

@app.get("/ping/{pong}")
async def test(pong):
    return {"message" : pong}