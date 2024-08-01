import logging
from aiogram import types
from init import dp
from init import render_template, redis_client
from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, HiddenItem, OrderItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_handlers():
    pass
