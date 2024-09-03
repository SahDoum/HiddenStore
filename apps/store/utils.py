from libs.hidden_client import (
    HiddenUser,
    HiddenOrder,
    HiddenMenu,
    HiddenItem,
    OrderItem,
)

from init import render_template
from config import ORDERS_PER_PAGE


def get_orders_page(orders: list, page: int) -> list:
    start = page * ORDERS_PER_PAGE
    end = start + ORDERS_PER_PAGE
    return orders[start:end]


async def get_order_messages(page: list, object_type) -> list[str]:
    obj_msgs = []
    for hidden_order in page:
        hidden_user = await object_type.get_or_create(id=hidden_order.order.user)
        obj_msgs.append(
            render_template(
                "order_info_store_short.txt",
                order=hidden_order.order,
                items=hidden_order.items(),
                user=hidden_user.user,
            )
        )
    return obj_msgs
