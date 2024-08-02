import os
import aiohttp
import random
from typing import Optional
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

# Загрузка токена из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
SERVER_URL = os.getenv("SERVER_URL", "http://server:8000")  # URL of the server service

# Настройка бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class Form(StatesGroup):
    name = State()
    user_id = State()  # Для хранения ID пользователя

# Пример списка печений
COOKIE_TYPES = ["chocolate_chip", "oatmeal", "peanut_butter", "gingerbread"]

async def get_user_id(telegram_id: str) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SERVER_URL}/users/telegram/{telegram_id}") as response:
            user_data = await response.json()
            return user_data.get('id')

async def create_order(user_id: str) -> dict:
    items = [{"type": random.choice(COOKIE_TYPES), "quantity": str(random.randint(1, 10))}]
    price = random.randint(100, 1000)
    order_data = {
        "items": items,
        "price": price,
        "user": user_id,
        "comment": None
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{SERVER_URL}/orders/", json=order_data) as response:
            return await response.json()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("Привет! Как тебя зовут?")

@dp.message_handler(commands='skip', state=Form.name)
async def cmd_skip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = 'друг'
        telegram_id = str(message.from_user.id)
        user_id = await get_user_id(telegram_id)
        if user_id:
            data['user_id'] = user_id
            await state.finish()
            await message.reply("Вы пропустили ввод имени. Добро пожаловать, друг!")
        else:
            await message.reply("Произошла ошибка при получении данных пользователя.")

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        telegram_id = str(message.from_user.id)
        user_id = await get_user_id(telegram_id)
        if user_id:
            data['user_id'] = user_id
            await state.finish()
            await message.reply(f"Приятно познакомиться, {message.text}!")
        else:
            await message.reply("Произошла ошибка при получении данных пользователя.")

@dp.message_handler(commands='name')
async def cmd_name(message: types.Message):
    await Form.name.set()
    await message.reply("Как тебя зовут?")

@dp.message_handler(commands='about')
async def cmd_about(message: types.Message):
    telegram_id = str(message.from_user.id)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SERVER_URL}/users/telegram/{telegram_id}") as response:
            user_data = await response.json()
            await message.reply(f"Информация о пользователе: {user_data}")

@dp.message_handler(commands='order')
async def cmd_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get('user_id')
    if user_id:
        order_response = await create_order(user_id)
        await message.reply(f"Ваш заказ оформлен! ID заказа: {order_response.get('id')}")
    else:
        await message.reply("Ошибка: ID пользователя не найден. Пожалуйста, сначала введите имя.")

@dp.message_handler(commands='orders')
async def cmd_orders(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get('user_id')
    if user_id:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/orders/user/{user_id}") as response:
                orders = await response.json()
                if isinstance(orders, list):
                    for order in orders:
                        await message.reply(f"Заказ: {order}")
                else:
                    await message.reply("Ошибка получения заказов.")
    else:
        await message.reply("Ошибка: ID пользователя не найден. Пожалуйста, сначала введите имя.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
