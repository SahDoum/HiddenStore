import logging

from libs.hidden_client import HiddenOrder, HiddenUser
from libs.models.statuses import OrderStatus

from init import bot, redis_client
from config import KITCHEN_TG_ID
from init import render_template


from keyboards import order_keyboard
from handlers.orders import orders_view


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_create(user_id, order_id):
    hidden_order = await HiddenOrder.get(order_id)
    if hidden_order is None:
        await bot.send_message(
            KITCHEN_TG_ID, "Пришел новый заказ, но что-то пошло не так, и его не покажу"
        )
        return

    user_data = None
    user = await hidden_order.user()
    if user is not None:
        user_data = user.data

    msg = "Пришел новый заказ: \n\n"
    msg += render_template(
        "order_info.txt",
        order=hidden_order.data,
        items=hidden_order.items(),
        user=user_data,
    )
    logger.error(msg)
    keyboard = order_keyboard(hidden_order.data, orders_view.callback)

    await bot.send_message(KITCHEN_TG_ID, msg, reply_markup=keyboard)


async def on_update(user_id, order_id):
    order = await HiddenOrder.get(order_id)
    if order is None:
        logger.error(f"on_update: Заказ {order_id} не сфетчился")
        return
    if order.data.status == OrderStatus.SHIPPED:
        user = await HiddenUser.get_or_create(id=order.data.user)

        if user is None:
            logger.error(f"on_update: Пользователь {order.data.user} не сфетчился")
            return

        await bot.send_message(user.data.telegram_id, "Заказ доставлен:")

        msg = render_template(
            "order_info.txt",
            order=order.data,
            items=order.items(),
            user=user,
        )
        await bot.send_message(user.data.telegram_id, msg)


async def register_notifiers():
    redis_client.listen(msg_type="create", callback=on_create)
