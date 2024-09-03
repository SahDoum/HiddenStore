import logging
from aiogram import types, F


from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
    HiddenPickupPoint,
)
from libs.models.statuses import OrderStatus

from init import dp, bot, render_template
from keyboards import orders_pagination_keyboard
from utils import get_orders_page, get_order_messages
from data import PageCallback, PickupPointDeleteCallback
from object_show_view import ObjectShowView

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


orders_view = ObjectShowView(HiddenOrder, "order", dp)
orders_callback = orders_view.callback


@orders_view.register_start
async def order_show_message(hidden_order):
    if hidden_order is None:
        return f"Заказ потерялся. Что-то пошло не так"

    hidden_user = await HiddenUser.get_or_create(id=hidden_order.order.user)

    msg = render_template(
        "order_info.txt",
        order=hidden_order.order,
        items=hidden_order.items(),
        user=hidden_user.user,
    )

    return msg


@orders_view.register("delete", "Удалить")
def order_delete_message(
    callback_query: types.CallbackQuery, callback_data: orders_callback
):
    pass


@orders_view.register("packed", "Запаковать")
async def process_callback(
    callback_query: types.CallbackQuery, callback_data: orders_callback
):
    hidden_order = await HiddenOrder.get(callback_data.object_id)

    if not hidden_order:
        await callback_query.answer(f"Заказ потерялся. Что-то пошло не так")
        return

    await hidden_order.update(status=OrderStatus.PACKED)

    await callback_query.message.reply("Запаковали!")


@orders_view.register("suport", "Открыть чат")
def order_support(callback_query: types.CallbackQuery, callback_data: orders_callback):
    pass


@dp.callback_query(PageCallback.filter())
async def process_callback_pagination(
    callback_query: types.CallbackQuery, callback_data: PageCallback
):
    page = callback_data.page
    orders = await HiddenOrder.list()

    if orders is None:
        await callback_query.answer(f"Страница потерялась. Что-то пошло не так")
        return

    orders_page = get_orders_page(orders, page)
    order_msgs = await get_order_messages(orders_page)
    msg = "Заказы: \n\n" + "\n".join(order_msgs)
    keyboard = orders_pagination_keyboard(orders, page, orders_view.callback)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=msg,
        reply_markup=keyboard,
    )


# Callback handler for pickup point deletion
@dp.callback_query(PickupPointDeleteCallback.filter())
async def process_delete_pickup_point(
    callback_query: types.CallbackQuery, callback_data: PickupPointDeleteCallback
):
    # Retrieve the pickup point ID
    pickup_point_id = callback_data.pickup_point_id

    # Placeholder: Call the delete method for the selected pickup point
    point = await HiddenPickupPoint.get(pickup_point_id)

    success = False
    if point:
        success = await point.delete()

    if success:
        await callback_query.answer(f"Пункт самовывоза удален.")
        await bot.edit_message_text(
            text=f"Пункт самовывоза удален.",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
        )
    else:
        await callback_query.answer("Ошибка при удалении пункта самовывоза.")


logger.error("Callbacks registered")
