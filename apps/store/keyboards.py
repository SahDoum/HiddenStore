from aiogram.utils.keyboard import InlineKeyboardBuilder
from libs.models.models import Order

from config import ORDERS_PER_PAGE
from utils import get_orders_page

from data import PageCallback, PickupPointDeleteCallback


def order_keyboard(order: Order, callback):
    builder = InlineKeyboardBuilder()

    builder.button(
        "Отгрузил, пусть приходит ->",
        callback_data=callback(object_id=order.id, action="packed"),
    )

    return builder.as_markup()


def orders_pagination_keyboard(orders: list, page: int, callback):
    builder = InlineKeyboardBuilder()
    orders_page = get_orders_page(orders, page)

    for hidden_order in orders_page:
        builder.button(
            text=hidden_order.order.id,
            callback_data=callback(action="show", object_id=hidden_order.order.id),
        )

    navigation_builder = InlineKeyboardBuilder()
    if page > 0:
        navigation_builder.button(
            text="<< Previous", callback_data=PageCallback(page=page - 1)
        )
    if (page + 1) * ORDERS_PER_PAGE < len(orders):  # edit
        navigation_builder.button(
            text="Next >>", callback_data=PageCallback(page=page + 1)
        )

    builder.attach(navigation_builder)

    return builder.as_markup()


def delete_pickup_point_keyboard(pickup_points: list):
    builder = InlineKeyboardBuilder()

    for pickup_point in pickup_points:
        builder.button(
            text=pickup_point.pickup_point.address,
            callback_data=PickupPointDeleteCallback(
                pickup_point_id=pickup_point.pickup_point.id
            ),
        )

    return builder.as_markup()
