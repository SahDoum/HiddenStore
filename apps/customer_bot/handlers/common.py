import random
from typing import Optional
from aiogram.dispatcher import FSMContext
from aiogram import types
from init import api
from templates.messages import MESSAGES

COOKIE_TYPES = ["chocolate_chip", "oatmeal", "peanut_butter", "gingerbread"]

async def get_user_id(telegram_id: str) -> Optional[str]:
    res = api.get_user_by_telegram_id(telegram_id)
    return res.get('id')

async def create_order(user_id: str) -> dict:
    items = [{"type": random.choice(COOKIE_TYPES), "quantity": str(random.randint(1, 10))}]
    price = random.randint(100, 1000)
    return api.create_order(items, price, user_id)
