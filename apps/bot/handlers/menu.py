import logging
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command
from aiogram import types


from libs.hidden_client import HiddenUser, HiddenMenu, HiddenItem, HiddenOrder

from templates.messages import MESSAGES

from init import dp, render_template


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderCallback(CallbackData, prefix="order"):
    item_id: str


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    menu = await HiddenMenu.get_items()
    if len(menu.hidden_items) > 0:
        menu_items = menu.items()

        builder = InlineKeyboardBuilder()
        for item in menu_items:
            builder.button(text=item.item, callback_data=OrderCallback(item_id=item.id))

        msg = render_template("menu.txt", items=menu_items)
        await message.reply(msg, reply_markup=builder.as_markup())
    else:
        await message.reply(MESSAGES["error_fetching_menu"])


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

    await callback_query.answer(f"Вы выбрали {item.data.item}")
    order = await HiddenOrder.create([(item.data, 1.0)], item.data.price, user)

    if not order:
        await callback_query.answer(f"Заказ не создался")
        return

    await callback_query.message.reply("Успех!")
