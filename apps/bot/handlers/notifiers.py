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
    user = await HiddenUser.get_or_create(id=order.data.user)

    if user is None:
        logger.error(f"on_update: Пользователь {order.data.user} не сфетчился")
        return

    if order.data.status == OrderStatus.PACKED:
        msg = "Заказ упакован: \n\n"
        msg += render_template("order_info.txt", order=order.data, items=order.items())
        await bot.send_message(user.data.telegram_id, msg)


async def on_create(user_id: str, order_id: str):
    hidden_order = await HiddenOrder.get(order_id)
    hidden_user = await HiddenUser.get(user_id)
    if hidden_order is None or hidden_user is None:
        return

    user_data = None
    user = await hidden_order.user()
    if user is not None:
        user_data = user.data

    msg = "Заказ создался: \n\n"
    msg += render_template(
        "order_info.txt",
        order=hidden_order.data,
        items=hidden_order.items(),
    )
    # keyboard = order_keyboard(hidden_order.data, orders_view.callback)
    await bot.send_message(hidden_user.data.telegram_id, msg)


async def register_notifiers():
    redis_client.listen(msg_type="update", callback=on_update)
