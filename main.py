from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette import status

from db.router import user_router
from modules.server import origins

app = FastAPI()

app.include_router(user_router.router)
app.mount("/static", StaticFiles(directory='./frontend/static'), name='static')

templates = Jinja2Templates(directory='./frontend/html')

# @app.get("/")
# async def root():
#     return {'2317' : "이강"}

@app.get("/ping/{pong}")
async def test(pong):
    return {"message" : pong}

@app.get("/f/{username}", response_class=HTMLResponse)
async def front_response(request: Request, username: str):
    return templates.TemplateResponse("./main.html", {'request' : request, 'name' : username})

@app.get('/register', response_class=HTMLResponse)
async def regist_response(request: Request):
    return templates.TemplateResponse("./register.html", {'request' : request})

@app.get('/login', response_class=HTMLResponse)
async def login_response(request: Request):
    return templates.TemplateResponse("./login.html", {'request' : request})

@app.get('/solo', response_class=HTMLResponse)
async def sprint_response(request : Request):
    return templates.TemplateResponse("{{ url_for('static', path='src/python/main.py') }}", {'request' : request})