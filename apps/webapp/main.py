import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from libs.hidden_client import APIConfig
from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
)

from config import SERVER_URL
from models import OrderData
from common import is_valid_data, make_items


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


templates = Jinja2Templates(directory="frontend/html")
APIConfig.setup(base_url=SERVER_URL)
app = FastAPI()

# setup routing

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    menu = await HiddenMenu.get_items()
    return templates.TemplateResponse(
        "cafe.html", {"request": request, "items": menu.items()}
    )


@app.post("/api/order")
async def order(request: OrderData):
    try:
        logger.error("/api/order")
        logger.error(request.dict())

        if not is_valid_data(request):
            logger.error("Invalid data")
            raise HTTPException(status_code=400, detail="Invalid data")

        logger.error("/api/order here")
        price = request.price

        user = await HiddenUser.get_or_create(telegram_id=request.user_id)
        items = await make_items(request.items)

        hidden_order = await HiddenOrder.create(items, price, user)
        logger.error("Order created")
        return hidden_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
