import logging
from aiogram import types
from init import dp
from templates.messages import MESSAGES
from init import render_template
from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, OrderItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply(MESSAGES['start'])


@dp.message_handler(commands='about')
async def cmd_about(message: types.Message):
    telegram_id = str(message.from_user.id)    
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)
    if not user:
        await message.reply(MESSAGES['error_fetching_user'])
        return
    msg = render_template('user_info.txt', user=user.user)
    await message.reply(msg)
        

@dp.message_handler(commands='order')
async def cmd_order(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)
    if not user:
        await message.reply(MESSAGES['error_fetching_user'])
        return
    items = [
        (OrderItem(item="Item1", count=1, details="Some details", price=100, unit="pcs"), 1),
    ]
    order = await HiddenOrder.create(items=items, price=100, user=user)
    await message.reply(MESSAGES['order_success'].format(order_id=order.order.id))


@dp.message_handler(commands='orders')
async def cmd_orders(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)
    if not user:
        await message.reply(MESSAGES['error_fetching_user'])
        return

    orders = await user.get_orders()
    if isinstance(orders, list):
        for order in orders:
            hidden_order = HiddenOrder(order, user)
            msg = render_template('order_info.txt', order=hidden_order.order, items=hidden_order.items())
            await message.reply(msg)
            return

    await message.reply(MESSAGES['error_orders'])


@dp.message_handler(commands='menu')
async def cmd_menu(message: types.Message):
    menu = await HiddenMenu.get_items()
    if isinstance(menu.items, list):
        msg = render_template('menu.txt', items=menu.items)
        await message.reply(msg)
    else:
        await message.reply(MESSAGES['error_fetching_menu'])


def register_handlers():
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_about, commands='about')
    dp.register_message_handler(cmd_order, commands='order', state="*")
    dp.register_message_handler(cmd_orders, commands='orders', state="*")
    dp.register_message_handler(cmd_menu, commands='menu', state="*")
