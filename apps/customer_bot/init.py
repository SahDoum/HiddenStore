from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

from jinja2 import Environment, FileSystemLoader

from config import TOKEN, REDIS_HOST, REDIS_PORT, SERVER_URL

import sys
import os
sys.path.append(os.path.abspath('.'))
from libs.hidden_client import APIClient, APIConfig

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
# api = APIClient(base_url=SERVER_URL)
APIConfig.setup(base_url=SERVER_URL)

template_loader = FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__), 'templates'))
template_env = Environment(loader=template_loader)

def render_template(template_name: str, *args, **kwargs):
    template = template_env.get_template(template_name)
    return template.render(*args, **kwargs)
