import logging

from libs.hidden_client import HiddenUser, HiddenOrder
from init import bot, redis_client
from init import render_template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_update(user_id, order_id):
    order = await HiddenOrder.get(order_id)
    if order is None:
        logger.error(f"Заказ {order_id} не сфетчился")
        return

    user = await HiddenUser.get_or_create(id=order.data.user)

    if user is None:
        logger.error(f"Пользователь {order.data.user} не сфетчился")
        return

    await bot.send_message(user.user.telegram_id, "Заказ упакован:")

    msg = render_template("order_info.txt", order=order.data, items=order.items())
    await bot.send_message(user.user.telegram_id, msg)


async def register_notifiers():
    redis_client.listen(msg_type="update", callback=on_update)
