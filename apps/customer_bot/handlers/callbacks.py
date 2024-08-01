import logging
from aiogram import types

from init import dp

from libs.hidden_client import HiddenUser, HiddenOrder, HiddenMenu, HiddenItem, OrderItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.callback_query_handler(lambda c: c.data.startswith('order_'))
async def process_callback(callback_query: types.CallbackQuery):

    item_id = callback_query.data.split('_')[1]
    item = await HiddenItem.get(item_id)

    if not item:
        await callback_query.answer(f"потерялся товар, обновите меню")
        return
    
    telegram_id = callback_query.from_user.id
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)

    logger.error("USER:")
    logger.error(user)

    if not user:
        await callback_query.answer(f"Не получилось создать пользователя")
        return
    
    await callback_query.answer(f"Вы выбрали {item.item.item}")
    order = await HiddenOrder.create([(item.item, 1.0)], item.item.price, user)

    if not order:
        await callback_query.answer(f"Заказ не создался")
        return
    
    await callback_query.message.reply("Успех!")

logger.error("Callbacks registered")
