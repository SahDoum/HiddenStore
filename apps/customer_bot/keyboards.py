from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from libs.models.models import OrderItem


def menu_keyboard(items: list[OrderItem]):
    keyboard = InlineKeyboardMarkup()

    for item in items:
        button = InlineKeyboardButton(text=item.item, callback_data=f"order_{item.id}")
        keyboard.add(button)

    return keyboard
