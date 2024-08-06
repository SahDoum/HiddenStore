import logging
from aiogram import types
from init import dp
from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
)

from utils import get_orders_page, get_order_messages
from keyboards import order_keyboard, orders_pagination_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message_handler(commands="orders")
async def cmd_orders(message: types.Message):
    orders = await HiddenOrder.list()
    if orders is None:
        await message.reply("Нет заказов")
        return

    orders_page = get_orders_page(orders, 0)
    order_msgs = await get_order_messages(orders_page)

    msg = "Заказы: \n\n" + "\n".join(order_msgs)

    keyboard = orders_pagination_keyboard(orders, 0)
    logger.error(msg)

    await message.reply(msg, reply_markup=keyboard)


logger.info("Commands registered")
