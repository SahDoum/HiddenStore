import logging

from aiogram import types
from aiogram.filters import Command


from templates.messages import MESSAGES
from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
)


from init import dp
from init import render_template
from keyboards import menu_keyboard, start_keyboard


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    telegram_id = str(message.from_user.id)
    username = None
    if message.from_user.username:
        username = message.from_user.username
    elif message.from_user.first_name:
        username = message.from_user.first_name

    await HiddenUser.get_or_create(telegram_id=telegram_id, name=username)
    await message.reply(MESSAGES["start"], reply_markup=start_keyboard())


@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)
    if not user:
        await message.reply(MESSAGES["error_fetching_user"])
        return
    msg = render_template("user_info.txt", user=user.data)
    await message.reply(msg)


@dp.message(Command("order"))
async def cmd_order(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)
    if not user:
        await message.reply(MESSAGES["error_fetching_user"])
        return
    items = [
        (
            OrderItem(
                item="Item1", count=1, details="Some details", price=100, unit="pcs"
            ),
            1.0,
        ),
    ]
    order = await HiddenOrder.create(items=items, price=100, user=user)
    await message.reply(MESSAGES["order_success"].format(order_id=order.data.id))


@dp.message(Command("orders"))
async def cmd_orders(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)
    if not user:
        await message.reply(MESSAGES["error_fetching_user"])
        return

    orders = await user.get_orders()
    if isinstance(orders, list):
        for order in orders:
            hidden_order = HiddenOrder(order, user)
            msg = render_template(
                "order_info.txt", order=hidden_order.data, items=hidden_order.items()
            )
            await message.reply(msg)
            return

    await message.reply(MESSAGES["error_orders"])


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    menu = await HiddenMenu.get_items()
    if len(menu.hidden_items) > 0:
        menu_items = menu.items()
        keyboard = menu_keyboard(menu_items)
        msg = render_template("menu.txt", items=menu_items)
        await message.reply(msg, reply_markup=keyboard)
    else:
        await message.reply(MESSAGES["error_fetching_menu"])


@dp.message(Command("create"))
async def cmd_create(message: types.Message):
    try:
        # Parse command arguments
        _, item_str, details_str, price_str, unit_str = message.text.split(maxsplit=4)
        price = int(price_str)

        created_item = await HiddenItem.create(item_str, details_str, price, unit_str)

        # Respond to the user
        await message.reply(
            f"Item created successfully!\n"
            f"ID: {created_item.data.id}\n"
            f"Item: {created_item.data.item}\n"
            f"Details: {created_item.data.details}\n"
            f"Price: {created_item.data.price}\n"
            f"Unit: {created_item.data.unit}",
        )
    except ValueError:
        await message.reply(
            "Invalid input. Please make sure to use the correct format: /create {item} {details} {price} {unit}."
        )
    except Exception as e:
        await message.reply(f"An error occurred: {e}")


logger.info("Commands registered")


# def register_handlers():
#     pass


#     dp.register_message(cmd_start, commands="start")
#     dp.register_message(cmd_about, commands="about")
#     dp.register_message(cmd_order, commands="order")
#     dp.register_message(cmd_orders, commands="orders")
#     dp.register_message(cmd_menu, commands="menu")
#     dp.register_message(cmd_create, commands="create")
