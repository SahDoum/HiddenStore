import redis.asyncio as redis
from jinja2 import Environment, FileSystemLoader

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums.parse_mode import ParseMode

from libs.hidden_client import APIConfig
from libs.hidden_redis import HiddenRedis
from libs.render_template import render_template


from config import TOKEN, REDIS_HOST, REDIS_PORT, SERVER_URL

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
storage = RedisStorage(redis_client)
dp = Dispatcher(storage=storage)

APIConfig.setup(base_url=SERVER_URL)
redis_client = HiddenRedis(host=REDIS_HOST, port=REDIS_PORT)
