import logging
from aiogram import types

from init import dp

from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, HiddenItem, OrderItem
from libs.models.statuses import OrderStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.callback_query_handler(lambda c: c.data.startswith('packed_'))
async def process_callback(callback_query: types.CallbackQuery):

    order_id = callback_query.data.split('_')[1]
    order = await HiddenOrder.get(order_id)

    if not order:
        await callback_query.answer(f"Заказ потерялся. Что-то пошло не так")
        return
    
    await order.update(status=OrderStatus.PACKED)

    await callback_query.message.reply("Запаковали!")

logger.error("Callbacks registered")
