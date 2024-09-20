import logging
from aiogram import types
from aiogram.fsm.context import FSMContext

from libs.hidden_client import HiddenUser, HiddenOrder

# from libs.models.schemas import OrderItemUpdate
from libs.telegram_views.object_show_view import ObjectShowView
from libs.telegram_views.paginator_view import Paginator

from init import dp, render_template


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


user_view = ObjectShowView(HiddenUser, "item", dp)
user_callback = user_view.callback


@user_view.register_start
async def order_show_message(hidden_user):
    msg = render_template("user_info.txt", user=hidden_user.data)

    return msg


@user_view.register_callback("show_orders", "Посмотреть заказы")
async def item_edit_name_button(
    callback_query: types.CallbackQuery,
    callback_data: user_callback,
    state: FSMContext,
    view: ObjectShowView,
):
    obj_id = callback_data.object_id
    user = await HiddenUser.get(id=obj_id)
    orders = await user.get_orders()

    for order in orders:
        hidden_order = HiddenOrder(order, user=user)
        msg = render_template(
            "order_info.txt",
            order=hidden_order.data,
            items=hidden_order.items(),
            user=user,
        )
        await callback_query.message.reply(msg)


@user_view.register_reply("edit_name")
async def item_edit_name(
    message: types.Message,
    state: FSMContext,
    view: ObjectShowView,
):
    state_data = await state.get_data()
    obj_id = state_data["obj_id"]
    hidden_item = await HiddenUser.get(id=obj_id)
    await state.clear()

    if hidden_item is None:
        await message.answer(f"что-то пошло не так")
        return

    res = await hidden_item.update(OrderItemUpdate(item=message.text))

    if not res:
        await message.answer(f"что-то пошло не так")
        return

    await message.answer(f"Обновлено на: {message.text}")


async def description_func(users: list[HiddenUser], first_index: int, state):
    order_msgs = []
    for hidden_user in users:
        first_index += 1
        msg = render_template("user_name.txt", user=hidden_user.data)
        order_msgs.append(msg)
    msg = "Пользователи: \n\n" + "\n".join(order_msgs)
    return msg


orders_paginator = Paginator(
    HiddenUser, user_view, "item", description_func, "items", dp
)

logger.info("Item View registered")
