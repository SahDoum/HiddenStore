from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from libs.models.models import Order


def order_keyboard(order: Order):
    keyboard = InlineKeyboardMarkup()

    button = InlineKeyboardButton(text="Отгрузил, пусть приходит ->", callback_data=f"packed_{order.id}")
    keyboard.add(button)

    return keyboard
