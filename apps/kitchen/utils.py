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


async def get_order_messages(orders_page: list) -> list[str]:
    order_msgs = []
    for hidden_order in orders_page:
        hidden_user = await HiddenUser.get_or_create(id=hidden_order.order.user)
        order_msgs.append(
            render_template(
                "order_info_store_short.txt",
                order=hidden_order.order,
                items=hidden_order.items(),
                user=hidden_user.user,
            )
        )
    return order_msgs
