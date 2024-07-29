from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from init import dp
from handlers.common import get_user_id, create_order
from templates.messages import MESSAGES
from init import api, render_template


class Form(StatesGroup):
    name = State()
    user_id = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    # await Form.name.set()
    await message.reply(MESSAGES['start'])

# @dp.message_handler(commands='skip', state=Form.name)
# async def cmd_skip(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['name'] = 'Anon'
#         telegram_id = str(message.from_user.id)
#         user_id = await get_user_id(telegram_id)
#         if user_id:
#             data['user_id'] = user_id
#             await state.finish()
#             await message.reply(MESSAGES['skip'])
#         else:
#             await message.reply(MESSAGES['error_user'])

# @dp.message_handler(state=Form.name)
# async def process_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['name'] = message.text
#         telegram_id = str(message.from_user.id)
#         user_id = await get_user_id(telegram_id)
#         if user_id:
#             data['user_id'] = user_id
#             await state.finish()
#             await message.reply(MESSAGES['greet'].format(name=message.text))
#         else:
#             await message.reply(MESSAGES['error_user'])

# @dp.message_handler(commands='name')
# async def cmd_name(message: types.Message):
#     await Form.name.set()
#     await message.reply(MESSAGES['name_prompt'])

@dp.message_handler(commands='about')
async def cmd_about(message: types.Message):
    await message.reply(MESSAGES['api_request'])
    telegram_id = str(message.from_user.id)
    user_data = api.get_user_by_telegram_id(telegram_id)
    await message.reply('билдим шаблон')
    msg = render_template('user_info.txt', user=user_data)
    await message.reply(msg)

@dp.message_handler(commands='order')
async def cmd_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get('user_id')
    if user_id:
        order_response = await create_order(user_id)
        await message.reply(MESSAGES['order_success'].format(order_id=order_response.get('id')))
    else:
        await message.reply(MESSAGES['error_user_id'])

@dp.message_handler(commands='orders')
async def cmd_orders(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data.get('user_id')
    if user_id:
        orders = api.get_orders_by_user(user_id)
        if isinstance(orders, list):
            for order in orders:
                msg = render_template('order_info.txt', order=order)
                await message.reply(msg)
        else:
            await message.reply(MESSAGES['error_orders'])
    else:
        await message.reply(MESSAGES['error_user_id'])

def register_handlers():
    dp.register_message_handler(cmd_start, commands='start')
    # dp.register_message_handler(cmd_skip, commands='skip', state=Form.name)
    # dp.register_message_handler(process_name, state=Form.name)
    # dp.register_message_handler(cmd_name, commands='name')
    dp.register_message_handler(cmd_about, commands='about')
    dp.register_message_handler(cmd_order, commands='order', state="*")
    dp.register_message_handler(cmd_orders, commands='orders', state="*")
