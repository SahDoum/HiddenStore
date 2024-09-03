import logging

from libs.hidden_client import HiddenItem

from init import dp
from object_create_view import ObjectCreateView

from object_show_view import ObjectShowView
from paginator_view import Paginator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


menu_item_factory = ObjectCreateView(
    HiddenItem,
    fields={
        "item": "Введите название товара:",
        "details": "Введите описание:",
        "price": "Введите стоимость:",
        "unit": "Введите, в чем измеряется (шт, гр):",
    },
    command_name="create_item",
    dp=dp,
)


async def description_func(items: list[HiddenItem]):
    order_msgs = []
    for hidden_item in items:
        order_msgs.append(f"{hidden_item.item.item}")
    msg = "Пункты меню: \n\n" + "\n".join(order_msgs)
    return msg


item_show_view = ObjectShowView(HiddenItem, "item", dp)

orders_paginator = Paginator(
    HiddenItem, item_show_view, "item", description_func, "items", dp
)

logger.info("Item View registered")
