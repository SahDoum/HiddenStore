from aiogram import Dispatcher
from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


from libs.hidden_client.wrappers import HiddenWrapper

from .utils import get_page, ORDERS_PER_PAGE

from init import bot

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PageCallback(CallbackData, prefix="page"):
    page: int
    obj_prefix: str


def orders_pagination_keyboard(
    orders: list, page: int, prefix: str, first_index: int, callback
):
    builder = InlineKeyboardBuilder()
    obj_page = get_page(orders, page)

    for item in obj_page:
        first_index += 1
        builder.button(
            text=f"{first_index}",
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
        object_type: HiddenWrapper,
        object_view,
        prefix: str,
        item_description_func,
        command: str,
        dp: Dispatcher,
        state_preparer=None,
        filter_objects=None,
    ) -> None:
        self.object_type = object_type
        self.object_view = object_view
        self.prefix = prefix
        self.item_description_func = item_description_func
        self.command = command
        self.dp = dp

        self.register_item_description(item_description_func)
        self.init_page_callback()
        self.state_preparer = state_preparer
        self.filter_objects = filter_objects

    def register_item_description(self, func):
        func = self.item_description_func

        @self.dp.message(Command(self.command))
        async def cmd_start(message: types.Message, state: FSMContext):
            if self.state_preparer is not None:
                await self.state_preparer(message, state)
            objects = await self.get_objects(state)
            if not objects:
                await message.reply(f"Ничего нет")
                return

            msg, keyboard = await self.render_page_and_keyboard(objects, 0, state)
            await message.reply(text=msg, reply_markup=keyboard)

        return func

    def init_page_callback(self):
        @self.dp.callback_query(PageCallback.filter(F.obj_prefix == self.prefix))  #
        async def process_callback_pagination(
            callback_query: types.CallbackQuery,
            callback_data: PageCallback,
            state: FSMContext,
        ):
            page = callback_data.page

            objects = await self.get_objects(state)

            if objects is None:
                await callback_query.answer(f"Страница потерялась. Что-то пошло не так")
                return

            msg, keyboard = await self.render_page_and_keyboard(objects, page, state)

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=msg,
                reply_markup=keyboard,
            )

    async def render_page_and_keyboard(self, objects, page: int, state: FSMContext):
        obj_page = get_page(objects, page)
        first_index = page * ORDERS_PER_PAGE
        msg = await self.item_description_func(obj_page, first_index, state)

        keyboard = orders_pagination_keyboard(
            objects, page, self.prefix, first_index, self.object_view.callback
        )

        return msg, keyboard

    async def get_objects(self, state: FSMContext) -> list[HiddenWrapper]:
        objects = await self.object_type.list()
        state_data = await state.get_data()

        if self.filter_objects:
            objects = self.filter_objects(objects, state_data)

        return objects
