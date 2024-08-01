from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import os
SERVER_URL = os.getenv("SERVER_URL", "http://server:8000")

import sys
sys.path.append(os.path.abspath('.'))
from libs.hidden_client import APIConfig
from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, HiddenItem, OrderItem
APIConfig.setup(base_url=SERVER_URL)


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/html")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    menu = await HiddenMenu.get_items()
    return templates.TemplateResponse("cafe.html", {"request": request, "items": menu.items()})
