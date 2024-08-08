from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from libs.models.models import OrderItem
from config import WEBAPP_URL


def menu_keyboard(items: list[OrderItem]):
    keyboard = InlineKeyboardMarkup()

    for item in items:
        button = InlineKeyboardButton(text=item.item, callback_data=f"order_{item.id}")
        keyboard.add(button)

    return keyboard


def start_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Заказать", web_app=WebAppInfo(url=WEBAPP_URL))
    keyboard.add(button)

    return keyboard
