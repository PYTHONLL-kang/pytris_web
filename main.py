from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from pydantic import BaseSettings

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette import status

import os
from db.router import user_router

class Setting(BaseSettings):
    APP_ENV : str = 'dev'

    class Config:
        env_file = '.env'

settings = Setting(_env_file='.env')
app = FastAPI()

app.include_router(user_router.router)
app.mount("/static", StaticFiles(directory='./frontend/static'), name='static')

templates = Jinja2Templates(directory='./frontend/html')

origins = {
    'pyg' : 'http://localhost:5000',
    'front' : 'http://localhost:5500',
    'back' : 'http://localhost:8000'
}

@app.get("/")
async def root():
    return Setting()

@app.get("/ping/{pong}")
async def test(pong):
    return {"message" : pong}

@app.get("/f/{username}", response_class=HTMLResponse)
async def front_response(username : str, request: Request):
    return templates.TemplateResponse("./main.html", {'request' : request, 'name' : username})

@app.get('/register', response_class=HTMLResponse)
async def regist_response(request: Request):
    return templates.TemplateResponse("./register.html", {'request' : request})

@app.get('/login', response_class=HTMLResponse)
async def login_response(request: Request):
    return templates.TemplateResponse("./login.html", {'request' : request})

# @app.get('/solo', response_class=HTMLResponse)
# async def sprint_response(request : Request):
#     return templates.TemplateResponse("{{ url_for('static', path='src/python/main.py') }}", {'request' : request})