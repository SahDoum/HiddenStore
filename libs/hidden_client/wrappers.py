import logging

from typing import Optional, List
import json

from .client import APIClient
from libs.models.schemas import (
    UserCreate,
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    OrderItemUpdate,
)
from libs.models.models import OrderItem, Order, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HiddenUser:
    def __init__(self, user: User):
        self.user = user

    @classmethod
    async def get_or_create(
        cls,
        id: Optional[str] = None,
        telegram_id: Optional[str] = None,
        name: Optional[str] = None,
    ):
        async with APIClient() as api_client:
            try:
                user = None
                if id:
                    user = await api_client.get_user_by_id(user_id=id)
                elif telegram_id:
                    user = await api_client.get_user_by_telegram_id(
                        telegram_id=telegram_id
                    )
            except Exception as e:
                if telegram_id:
                    user_data = UserCreate(name=name, telegram_id=telegram_id)
                    user = await api_client.create_user(user_data=user_data)
            finally:
                return cls(User.parse_obj(user))

    async def get_orders(self) -> List[Order]:
        async with APIClient() as api_client:
            try:
                orders = await api_client.get_orders_by_user(user_id=self.user.id)
                return [Order.parse_obj(order) for order in orders]
            except:
                return []


class HiddenOrder:
    def __init__(self, order: Order, user: HiddenUser = None):
        self.order = order
        self.user = user

    @classmethod
    async def create(
        cls,
        items: list[tuple[OrderItem, float]],
        price: int,
        user: HiddenUser,
        comment: Optional[str] = None,
    ):
        async with APIClient() as api_client:
            order_data = OrderCreate(
                items=[
                    (cls.item_to_str(item[0]), item[1]) for item in items
                ],  # Convert OrderItem to dict and keep count
                price=price,
                user=user.user.id,  # Use the user ID from HiddenUser
                comment=comment,
            )
            order = await api_client.create_order(order_data=order_data)
        return cls(Order.parse_obj(order))

    @classmethod
    async def get(cls, order_id: str):
        async with APIClient() as api_client:
            try:
                order = await api_client.get_order_by_id(order_id)
                return cls(Order.parse_obj(order))
            except:
                return None

    async def update(
        self,
        review: Optional[str] = None,
        comment: Optional[str] = None,
        is_delivered: Optional[bool] = None,
        is_paid: Optional[bool] = None,
        price: Optional[int] = None,
        status: Optional[str] = None,
    ):
        async with APIClient() as api_client:
            order_update = OrderUpdate(
                review=review,
                comment=comment,
                is_delivered=is_delivered,
                is_paid=is_paid,
                price=price,
                status=status,
            )
            updated_order = await api_client.update_order(
                order_id=self.order.id, order_update=order_update
            )
        self.order = Order.parse_obj(updated_order)
        return self.order

    @staticmethod
    def item_to_str(item: OrderItem) -> str:
        return json.dumps(item.model_dump(mode="json"))

    @staticmethod
    def str_to_item(item_str: str) -> OrderItem:
        logger.error(json.loads(item_str))
        return OrderItem.parse_obj(json.loads(item_str))

    def items(self) -> list[tuple[OrderItem, float]]:
        return [(self.str_to_item(item), count) for item, count in self.order.items]

    @classmethod
    async def list(cls):
        async with APIClient() as api_client:
            try:
                orders = await api_client.get_orders()
                return [cls(Order.parse_obj(order)) for order in orders]
            except:
                return None


class HiddenItem:
    def __init__(self, item: OrderItem):
        self.item = item

    @classmethod
    async def create(
        cls, item: str, details: Optional[str], price: int, unit: str
    ) -> "HiddenItem":
        async with APIClient() as api_client:
            item_data = OrderItemCreate(
                item=item, details=details, price=price, unit=unit
            )
            created_item = await api_client.create_menu_item(item_data)
        return cls(OrderItem.parse_obj(created_item))

    @classmethod
    async def get(cls, item_id: str) -> Optional["HiddenItem"]:
        async with APIClient() as api_client:
            item_data = await api_client.get_menu_item(item_id)
        return cls(OrderItem.parse_obj(item_data)) if item_data else None

    async def update(self, item_data: OrderItemUpdate) -> bool:
        async with APIClient() as api_client:
            updated_item = await api_client.update_menu_item(self.item.id, item_data)
        if updated_item:
            self.item = OrderItem.parse_obj(updated_item)
            return True
        return False

    async def delete(self) -> bool:
        async with APIClient() as api_client:
            success = await api_client.delete_menu_item(self.item.id)
        return success


class HiddenMenu:
    def __init__(self, items: List[OrderItem]):
        self.hidden_items = [HiddenItem(item) for item in items]

    @classmethod
    async def get_items(cls) -> "HiddenMenu":
        async with APIClient() as api_client:
            try:
                items = await api_client.get_menu_items()
                return cls([OrderItem.parse_obj(item) for item in items])
            except:
                return cls([])

    def items(self) -> list[OrderItem]:
        return [item.item for item in self.hidden_items]

    # async def update_items(self) -> bool:
    #     async with APIClient() as api_client:
    #         success = await api_client.update_menu_items(items=[item.item.dict() for item in self.hidden_items])
    #     return success
