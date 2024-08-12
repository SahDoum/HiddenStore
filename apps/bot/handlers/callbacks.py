import logging
from aiogram import types
from aiogram.filters.callback_data import CallbackData


from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenItem,
)


from init import dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderCallback(CallbackData, prefix="order"):
    item_id: str


@dp.callback_query(OrderCallback.filter())
async def process_callback(
    callback_query: types.CallbackQuery, callback_data: OrderCallback
):
    item = await HiddenItem.get(callback_data.item_id)

    if not item:
        await callback_query.answer(f"потерялся товар, обновите меню")
        return

    telegram_id = callback_query.from_user.id
    user = await HiddenUser.get_or_create(telegram_id=telegram_id)

    if not user:
        await callback_query.answer(f"Не получилось создать пользователя")
        return

    await callback_query.answer(f"Вы выбрали {item.item.item}")
    order = await HiddenOrder.create([(item.item, 1.0)], item.item.price, user)

    if not order:
        await callback_query.answer(f"Заказ не создался")
        return

    await callback_query.message.reply("Успех!")


logger.info("Callbacks registered")
