import logging

from libs.hidden_client import HiddenUser, HiddenOrder
from init import bot, redis_client
from init import render_template
from libs.models.statuses import OrderStatus


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_update(user_id, order_id):
    order = await HiddenOrder.get(order_id)
    if order is None:
        logger.error(f"on_update: Заказ {order_id} не сфетчился")
        return
    if order.data.status == OrderStatus.PACKED:
        user = await HiddenUser.get_or_create(id=order.data.user)

        if user is None:
            logger.error(f"on_update: Пользователь {order.data.user} не сфетчился")
            return

        await bot.send_message(user.data.telegram_id, "Заказ упакован:")

        msg = render_template("order_info.txt", order=order.data, items=order.items())
        await bot.send_message(user.data.telegram_id, msg)


async def register_notifiers():
    redis_client.listen(msg_type="update", callback=on_update)
