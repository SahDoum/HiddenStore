import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from init import dp
from templates.messages import MESSAGES
from init import render_template
from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, OrderItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Form(StatesGroup):
    name = State()
    user_id = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply(MESSAGES['start'])

@dp.message_handler(commands='about')
async def cmd_about(message: types.Message):
    await message.reply(MESSAGES['api_request'])
    telegram_id = str(message.from_user.id)
    
    try:
        user = await HiddenUser.get_or_create(telegram_id=telegram_id)
        msg = render_template('user_info.txt', user=user)
        await message.reply(msg)
    except Exception as e:
        logger.error(f"Error fetching user by telegram_id: {telegram_id}, error: {e}")
        await message.reply(MESSAGES['error_fetching_user'])

@dp.message_handler(commands='order')
async def cmd_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get('user_id')
    if user_id:
        try:
            items = [
                OrderItem(item="Item1", count=1, details="Some details", price=100, unit="pcs"),
            ]  # Replace with actual items or fetch from the state/context
            order = await HiddenOrder.create(items=items, price=100, user=user_id)  # Adjust price and items as needed
            await message.reply(MESSAGES['order_success'].format(order_id=order.id))
        except Exception as e:
            logger.error(f"Error creating order for user_id: {user_id}, error: {e}")
            await message.reply(MESSAGES['error_creating_order'])
    else:
        await message.reply(MESSAGES['error_user_id'])

@dp.message_handler(commands='orders')
async def cmd_orders(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get('user_id')
    if user_id:
        try:
            user = await HiddenUser.get_or_create(id=user_id)
            orders = await user.get_orders()
            if isinstance(orders, list):
                for order in orders:
                    logging.error("Заказ")
                    logging.error(order.items)
                    msg = render_template('order_info.txt', order=order.order_data)
                    await message.reply(msg)
            else:
                await message.reply(MESSAGES['error_orders'])
        except Exception as e:
            logger.error(f"Error fetching orders for user_id: {user_id}, error: {e}")
            await message.reply(MESSAGES['error_fetching_orders'])
    else:
        await message.reply(MESSAGES['error_user_id'])

@dp.message_handler(commands='menu')
async def cmd_menu(message: types.Message):
    try:
        menu = await HiddenMenu.get_items()
        if isinstance(menu.items, list):
            msg = render_template('menu.txt', items=menu.items)
            await message.reply(msg)
        else:
            await message.reply(MESSAGES['error_fetching_menu'])
    except Exception as e:
        logger.error(f"Error fetching menu items, error: {e}")
        await message.reply(MESSAGES['error_fetching_menu'])

def register_handlers():
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_about, commands='about')
    dp.register_message_handler(cmd_order, commands='order', state="*")
    dp.register_message_handler(cmd_orders, commands='orders', state="*")
    dp.register_message_handler(cmd_menu, commands='menu', state="*")
