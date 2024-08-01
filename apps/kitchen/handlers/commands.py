import logging
from aiogram import types
from init import dp
from init import render_template
from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, HiddenItem, OrderItem
from keyboards import order_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message_handler(commands='orders')
async def cmd_orders(message: types.Message):
    orders = await HiddenOrder.list()
    if orders is not None:
        for hidden_order in orders:
            msg = render_template('order_info.txt', order=hidden_order.order, items=hidden_order.items())
            keyboard = order_keyboard(hidden_order.order)
            await message.reply(msg, reply_markup=keyboard)
            return

    await message.reply("Нет заказов")

def register_handlers():
    pass
