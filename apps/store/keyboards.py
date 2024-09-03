from aiogram.utils.keyboard import InlineKeyboardBuilder
from libs.models.models import Order


def order_keyboard(order: Order, callback):
    builder = InlineKeyboardBuilder()

    builder.button(
        "Отгрузил, пусть приходит ->",
        callback_data=callback(object_id=order.id, action="packed"),
    )

    return builder.as_markup()
