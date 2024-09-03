from aiogram.filters.callback_data import CallbackData


class PageCallback(CallbackData, prefix="page"):
    page: int


# Callback data for pickup point deletion
class PickupPointDeleteCallback(CallbackData, prefix="delete_pickup_point"):
    pickup_point_id: str
