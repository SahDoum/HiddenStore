import logging

from aiogram import types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


from templates.messages import MESSAGES
from libs.hidden_client import HiddenUser


from init import dp


from config import WEBAPP_URL


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Заказать", web_app=WebAppInfo(url=WEBAPP_URL))

    return builder.as_markup()


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


logger.info("Commands registered")
