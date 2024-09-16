from aiogram.fsm.state import State, StatesGroup
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from aiogram.filters import Command


class ObjectCreateView:
    fields: dict[str, str]

    def __init__(self, model, fields: dict[str, str], command_name, dp: Dispatcher):
        self.model = model
        self.fields = fields
        self.command_name = command_name
        self.dp = dp

        # Dynamically create the StatesGroup class
        self.state_class = self.create_states_class()

        # Register handlers
        self.register_handlers()

    def create_states_class(self):
        class DynamicStates(StatesGroup):
            pass

        # Dynamically add states to the class
        for field_name in self.fields:
            setattr(DynamicStates, field_name, State(field_name))

        return DynamicStates

    def register_handlers(self):
        # Register the command handler to start the process
        self.dp.message(Command(self.command_name))(self.start_creation)

        # Register handlers for each field
        for field_name in self.fields:
            state = getattr(self.state_class, field_name)
            self.dp.message(state)(self.create_field_handler(field_name))

        fields_list = list(self.fields.keys())

    async def start_creation(self, message: types.Message, state: FSMContext):
        if not self.fields:
            await message.answer("Нет полей для создания объекта.")
            return

        first_field = next(iter(self.fields))

        if first_field is None:
            await message.answer("Не удалось определить начальное поле.")
            return

        await state.set_state(self.state_class.__dict__[first_field])
        await message.answer(self.fields[first_field])

    def create_field_handler(self, field: str):
        async def process_field(message: types.Message, state: FSMContext):
            await state.update_data({field: message.text})
            fields_list = list(self.fields.keys())
            current_index = fields_list.index(field)

            if current_index + 1 < len(fields_list):
                next_field = fields_list[current_index + 1]
                await message.answer(self.fields[next_field])
                await state.set_state(getattr(self.state_class, next_field))
            else:
                # If all fields are collected, create the object
                await self.finish_creation(message, state)

        return process_field

    async def finish_creation(self, message: types.Message, state: FSMContext):
        user_data = await state.get_data()

        if not user_data:
            await message.answer("Не удалось создать объект. Данные отсутствуют.")
            return

        obj = await self.model.create(**user_data)

        await state.clear()

        confirmation_message = "\n".join(
            [f"{key.capitalize()}: {value}" for key, value in user_data.items()]
        )
        await message.answer(f"Объект создан:\n\n{confirmation_message}")
