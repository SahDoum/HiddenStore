from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from libs.models.models import OrderItem

from handlers.callbacks import OrderCallback
from config import WEBAPP_URL


def menu_keyboard(items: list[OrderItem]):
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item.item, callback_data=OrderCallback(item_id=item.id))

    return builder.as_markup()


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Заказать", web_app=WebAppInfo(url=WEBAPP_URL))

    return builder.as_markup()
