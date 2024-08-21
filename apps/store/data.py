from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup


class OrderCallback(CallbackData, prefix="order"):
    action: str
    order_id: str


class PageCallback(CallbackData, prefix="page"):
    page: int


# Callback data for pickup point deletion
class PickupPointDeleteCallback(CallbackData, prefix="delete_pickup_point"):
    pickup_point_id: str


# Define states for the scenario
class PickupPointState(StatesGroup):
    address = State()
    description = State()
