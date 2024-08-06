from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from libs.models.models import Order

from config import ORDERS_PER_PAGE
from apps.kitchen.utils import get_orders_page


def order_keyboard(order: Order) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    button = InlineKeyboardButton(
        text="Отгрузил, пусть приходит ->", callback_data=f"order-packed_{order.id}"
    )
    keyboard.add(button)

    return keyboard


def orders_pagination_keyboard(orders: list, page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    orders_page = get_orders_page(orders, page)

    for hidden_order in orders_page:
        keyboard.add(
            InlineKeyboardButton(
                hidden_order.order.id,
                callback_data=f"order-show_{hidden_order.order.id}",
            )
        )

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton("<< Previous", callback_data=f"page_{page - 1}")
        )
    if (page + 1) * ORDERS_PER_PAGE < len(orders):  # edit
        navigation_buttons.append(
            InlineKeyboardButton("Next >>", callback_data=f"page_{page + 1}")
        )

    if navigation_buttons:
        keyboard.row(*navigation_buttons)

    return keyboard


def order_edit_keyboard(order: Order) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(text="Отгрузил", callback_data=f"order-packed_{order.id}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"order_delete_{order.id}"),
        InlineKeyboardButton(
            text="Открыть чат", callback_data=f"order-support_{order.id}"
        ),
        InlineKeyboardButton(text="<< К списку заказов", callback_data=f"page_0"),
    )

    return keyboard
