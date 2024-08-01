import logging

from libs.hidden_client import HiddenUser, HiddenOrder
from init import bot, redis_client
from config import KITCHEN_TG_ID
from init import render_template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_create(user_id, order_id):
    hidden_order = await HiddenOrder.get(order_id)

    await bot.send_message(KITCHEN_TG_ID, f"Новый заказ. Id: {order_id}") 
    if not hidden_order:
        await bot.send_message(KITCHEN_TG_ID, "заказ не сфетчился") 
        return

    msg = render_template('order_info.txt', order=hidden_order.order, items=hidden_order.items())
    await bot.send_message(KITCHEN_TG_ID, msg) 


def register_callbacks():
    redis_client.listen(msg_type="create", callback=on_create)
