import logging
from aiogram import types
from init import dp
from templates.messages import MESSAGES
from init import render_template, redis_client
from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, HiddenItem, OrderItem

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
        (OrderItem(item="Item1", count=1, details="Some details", price=100, unit="pcs"), 1.0),
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
    if len(menu.hidden_items) > 0:
        msg = render_template('menu.txt', items=menu.items())
        await message.reply(msg)
    else:
        await message.reply(MESSAGES['error_fetching_menu'])

# @dp.message_handler(commands='redis')
# async def cmd_redis(message: types.Message):
#     telegram_id = str(message.from_user.id)
#     user = await HiddenUser.get_or_create(telegram_id=telegram_id)
#     await redis_client.publish('create', user)

@dp.message_handler(commands='create')
async def cmd_create(message: types.Message):
    try:
        # Parse command arguments
        _, item_str, details_str, price_str, unit_str = message.text.split(maxsplit=4)
        price = int(price_str)

        created_item = await HiddenItem.create(item_str, details_str, price, unit_str)
        
        # Respond to the user
        await message.reply(
            f"Item created successfully!\n"
            f"ID: {created_item.item.id}\n"
            f"Item: {created_item.item.item}\n"
            f"Details: {created_item.item.details}\n"
            f"Price: {created_item.item.price}\n"
            f"Unit: {created_item.item.unit}",
        )
    except ValueError:
        await message.reply("Invalid input. Please make sure to use the correct format: /create {item} {details} {price} {unit}.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")



def register_handlers():
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_about, commands='about')
    dp.register_message_handler(cmd_order, commands='order')
    dp.register_message_handler(cmd_orders, commands='orders')
    dp.register_message_handler(cmd_menu, commands='menu')
    dp.register_message_handler(cmd_create, commands='create')
    # dp.register_message_handler(cmd_redis, commands='redis')
