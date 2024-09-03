from aiogram import Dispatcher
from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ORDERS_PER_PAGE
from utils import get_page
from init import bot


class PageCallback(CallbackData, prefix="page"):
    page: int
    obj_prefix: str


def orders_pagination_keyboard(orders: list, page: int, prefix: str, callback):
    builder = InlineKeyboardBuilder()
    obj_page = get_page(orders, page)

    for item in obj_page:
        builder.button(
            text=item.data.id,
            callback_data=callback(action="show", object_id=item.data.id),
        )

    navigation_builder = InlineKeyboardBuilder()
    if page > 0:
        navigation_builder.button(
            text="<< Previous",
            callback_data=PageCallback(page=page - 1, obj_prefix=prefix),
        )
    if (page + 1) * ORDERS_PER_PAGE < len(orders):  # edit
        navigation_builder.button(
            text="Next >>", callback_data=PageCallback(page=page + 1, obj_prefix=prefix)
        )

    builder.attach(navigation_builder)

    return builder.as_markup()


class Paginator:
    def __init__(
        self,
        object_type,
        object_view,
        prefix: str,
        item_description_func,
        command: str,
        dp: Dispatcher,
    ) -> None:
        self.object_type = object_type
        self.object_view = object_view
        self.prefix = prefix
        self.item_description_func = item_description_func
        self.command = command
        self.dp = dp

        self.register_item_description(item_description_func)
        self.init_page_callback()

    def register_item_description(self, func):
        func = self.item_description_func

        @self.dp.message(Command(self.command))
        async def cmd_start(message: types.Message):
            objects = await self.object_type.list()
            if objects is None:
                await message.reply(f"Нет")
                return

            msg, keyboard = await self.render_page_and_keyboard(objects, 0)
            await message.reply(text=msg, reply_markup=keyboard)

        return func

    def init_page_callback(self):
        @self.dp.callback_query(PageCallback.filter(F.obj_prefix == self.prefix))  #
        async def process_callback_pagination(
            callback_query: types.CallbackQuery, callback_data: PageCallback
        ):
            page = callback_data.page

            objects = await self.object_type.list()

            if objects is None:
                await callback_query.answer(f"Страница потерялась. Что-то пошло не так")
                return

            msg, keyboard = await self.render_page_and_keyboard(objects, page)

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=msg,
                reply_markup=keyboard,
            )

    async def render_page_and_keyboard(self, objects, page: int):
        obj_page = get_page(objects, page)
        msg = await self.item_description_func(obj_page)

        keyboard = orders_pagination_keyboard(
            objects, page, self.prefix, self.object_view.callback
        )

        return msg, keyboard
