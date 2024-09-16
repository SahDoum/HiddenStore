import logging
from aiogram import types
from aiogram.fsm.context import FSMContext


from libs.hidden_client import HiddenUser, HiddenOrder
from libs.models.statuses import OrderStatus
from libs.telegram_views.object_show_view import ObjectShowView
from libs.telegram_views.paginator_view import Paginator

from init import dp, render_template


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


orders_view = ObjectShowView(HiddenOrder, "order", dp)
orders_callback = orders_view.callback


@orders_view.register_start
async def order_show_message(hidden_order):
    if hidden_order is None:
        return f"Заказ потерялся. Что-то пошло не так"

    hidden_user = await HiddenUser.get_or_create(id=hidden_order.data.user)

    msg = render_template(
        "order_info.txt",
        order=hidden_order.data,
        items=hidden_order.items(),
        user=hidden_user.data,
    )

    return msg


@orders_view.register_callback("delete", "Удалить")
def order_delete_message(
    callback_query: types.CallbackQuery,
    callback_data: orders_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    pass


@orders_view.register_callback("packed", "Запаковать")
async def process_callback(
    callback_query: types.CallbackQuery,
    callback_data: orders_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    hidden_order = await HiddenOrder.get(callback_data.object_id)

    if not hidden_order:
        await callback_query.answer(f"Заказ потерялся. Что-то пошло не так")
        return

    await hidden_order.update(status=OrderStatus.PACKED)

    await callback_query.message.reply("Запаковали!")


@orders_view.register_callback("suport", "Открыть чат")
def order_support(
    callback_query: types.CallbackQuery,
    callback_data: orders_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    pass


async def description_func(orders, first_index):
    order_msgs = []
    for hidden_order in orders:
        first_index += 1
        hidden_user = await HiddenUser.get_or_create(id=hidden_order.data.user)
        order_msgs.append(
            f"{first_index}."
            + render_template(
                "order_info_store_short.txt",
                order=hidden_order.data,
                items=hidden_order.items(),
                user=hidden_user.data,
            )
        )
    msg = "Заказы: \n\n" + "\n".join(order_msgs)

    return msg


orders_paginator = Paginator(
    HiddenOrder, orders_view, "order", description_func, "orders", dp
)

logger.info("Order View registered")
