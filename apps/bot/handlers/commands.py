import logging

from aiogram import types
from aiogram.filters import Command


from templates.messages import MESSAGES
from libs.hidden_client import HiddenUser, HiddenMenu


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


logger.info("Commands registered")
