import logging

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, types
from aiogram.filters.callback_data import CallbackData
from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .paginator_view import PageCallback
from libs.hidden_client import HiddenWrapper

from init import dp, bot


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ObjectShowView:
    DefaultStartFilter = "show"
    state_group: StatesGroup

    def __init__(self, object_type: HiddenWrapper, prefix: str, dp: Dispatcher):
        self.object_type: HiddenWrapper = object_type
        self.dp: Dispatcher = dp
        self.prefix: str = prefix
        self.state: str = ""

        self.methods: dict[str, str] = {}

        class ActionsCallback(CallbackData, prefix=prefix):
            object_id: str
            action: str

        self.callback = ActionsCallback

        class ActionsState(StatesGroup):
            action = State()
            obj_id = State()

        self.state_group = ActionsState

        self.state_filter = StateFilter

    def register_callback(self, name: str, description: str):
        def decorator(func):
            async def wrapper(
                callback_query: types.CallbackQuery,
                callback_data: CallbackData,
                state: FSMContext,
            ):
                return await func(callback_query, callback_data, state, self)

            self.methods[name] = description
            dp.callback_query(self.callback.filter(F.action == name))(wrapper)
            return wrapper

        return decorator

    def register_reply(self, state: str):
        def decorator(func):
            async def wrapper(message: types.Message, state: FSMContext):
                return await func(message, state, self)

            self.dp.message(StateFilter(f"action:{state}"))(wrapper)
            return wrapper

        return decorator

    def register_start(self, func):
        @dp.callback_query(self.callback.filter(F.action == self.DefaultStartFilter))
        async def show_func(
            callback_query: types.CallbackQuery, callback_data: self.callback
        ):
            obj = await self.object_type.get(callback_data.object_id)

            if obj is None:
                await callback_query.answer(f"Заказ потерялся. Что-то пошло не так")
                return

            keyboard = self.keyboard(callback_data.object_id)
            msg = await func(obj)

            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=msg,
                reply_markup=keyboard,
            )

        return func

    async def set_state(self, state: StatesGroup, action: str, obj_id: str):
        await state.update_data(obj_id=obj_id)
        await state.set_state(f"action:{action}")

    def keyboard(self, object_id: str):
        builder = InlineKeyboardBuilder()

        for name, description in self.methods.items():
            builder.button(
                text=description,
                callback_data=self.callback(action=name, object_id=object_id),
            )
        # rewrite
        builder.button(
            text="<< К списку заказов",
            callback_data=PageCallback(page=0, obj_prefix=self.prefix),
        )
        builder.adjust(3, repeat=True)

        return builder.as_markup()
