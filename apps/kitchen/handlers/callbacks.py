import logging
from aiogram import types


from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
)
from libs.models.statuses import OrderStatus


from init import dp, bot, render_template
from keyboards import orders_pagination_keyboard, order_edit_keyboard
from utils import get_orders_page, get_order_messages


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.callback_query_handler(lambda c: c.data.startswith("order-packed_"))
async def process_callback(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split("_")[1]
    order = await HiddenOrder.get(order_id)

    if not order:
        await callback_query.answer(f"Заказ потерялся. Что-то пошло не так")
        return

    await order.update(status=OrderStatus.PACKED)

    await callback_query.message.reply("Запаковали!")


@dp.callback_query_handler(lambda c: c.data.startswith("page_"))
async def process_callback_pagination(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    orders = await HiddenOrder.list()

    if orders is None:
        await callback_query.answer(f"Страница потерялась. Что-то пошло не так")
        return

    orders_page = get_orders_page(orders, page)
    order_msgs = await get_order_messages(orders_page)
    msg = "Заказы: \n\n" + "\n".join(order_msgs)
    keyboard = orders_pagination_keyboard(orders, page)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=msg,
        reply_markup=keyboard,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("order-show_"))
async def process_callback_order_show(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split("_")[1]

    hidden_order = await HiddenOrder.get(order_id)

    if hidden_order is None:
        await callback_query.answer(f"Заказ потерялся. Что-то пошло не так")
        return

    hidden_user = await HiddenUser.get_or_create(id=hidden_order.order.user)

    msg = render_template(
        "order_info.txt",
        order=hidden_order.order,
        items=hidden_order.items(),
        user=hidden_user.user,
    )
    keyboard = order_edit_keyboard(hidden_order.order)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=msg,
        reply_markup=keyboard,
    )


logger.error("Callbacks registered")
