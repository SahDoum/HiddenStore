# server/api.py
from sqlmodel import select
from typing import Optional, Any
from libs.models.models import User, Order, OrderItem
from libs.models.schemas import (
    UserCreate,
    UserUpdate,
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    OrderItemUpdate,
)
from .db_config import get_session
import datetime


class UserAPI:
    @staticmethod
    async def create(data: UserCreate) -> User:
        async with await get_session() as session:
            user = User(name=data.name, telegram_id=data.telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get(user_id: str) -> Optional[User]:
        async with await get_session() as session:
            return await session.get(User, user_id)

    @staticmethod
    async def get_by_telegram_id(telegram_id: str) -> Optional[User]:
        async with await get_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def get_all() -> list[User]:
        async with await get_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    @staticmethod
    async def update(user_id: str, data: UserUpdate) -> Optional[User]:
        async with await get_session() as session:
            user = await session.get(User, user_id)
            if user:
                if data.name is not None:
                    user.name = data.name
                if data.telegram_id is not None:
                    user.telegram_id = data.telegram_id
                user.timestamp_updated = datetime.datetime.now()
                await session.commit()
                await session.refresh(user)
            return user

    @staticmethod
    async def delete(user_id: str) -> bool:
        async with await get_session() as session:
            user = await session.get(User, user_id)
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False


class OrderAPI:
    @staticmethod
    async def create(data: OrderCreate) -> Order:
        async with await get_session() as session:
            order = Order(
                items=data.items, price=data.price, user=data.user, comment=data.comment
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    @staticmethod
    async def get(order_id: str) -> Optional[Order]:
        async with await get_session() as session:
            return await session.get(Order, order_id)

    @staticmethod
    async def get_all() -> list[Order]:
        async with await get_session() as session:
            result = await session.execute(select(Order))
            return result.scalars().all()

    @staticmethod
    async def get_by_user(user_id: str) -> list[Order]:
        async with await get_session() as session:
            result = await session.execute(select(Order).where(Order.user == user_id))
            return result.scalars().all()

    @staticmethod
    async def update(order_id: str, data: OrderUpdate) -> Optional[Order]:
        async with await get_session() as session:
            order = await session.get(Order, order_id)
            if order:
                if data.review is not None:
                    order.review = data.review
                if data.comment is not None:
                    order.comment = data.comment
                if data.is_delivered is not None:
                    order.is_delivered = data.is_delivered
                if data.is_paid is not None:
                    order.is_paid = data.is_paid
                if data.price is not None:
                    order.price = data.price
                if data.status is not None:
                    order.status = data.status
                order.timestamp_updated = datetime.datetime.now()
                await session.commit()
                await session.refresh(order)
            return order

    @staticmethod
    async def delete(order_id: str) -> bool:
        async with await get_session() as session:
            order = await session.get(Order, order_id)
            if order:
                await session.delete(order)
                await session.commit()
                return True
            return False


class ItemsAPI:
    @staticmethod
    async def create(data: OrderItemCreate) -> OrderItem:
        async with await get_session() as session:
            item = OrderItem(
                item=data.item,
                amount=data.amount,
                details=data.details,
                price=data.price,
                unit=data.unit,
            )
            session.add(item)
            await session.commit()
            await session.refresh(item)
            return item

    @staticmethod
    async def get(item_id: str) -> Optional[OrderItem]:
        async with await get_session() as session:
            return await session.get(OrderItem, item_id)

    @staticmethod
    async def get_all() -> list[OrderItem]:
        async with await get_session() as session:
            result = await session.execute(select(OrderItem))
            return result.scalars().all()

    @staticmethod
    async def update(item_id: str, data: OrderItemUpdate) -> Optional[OrderItem]:
        async with await get_session() as session:
            item = await session.get(OrderItem, item_id)
            if item:
                if data.item is not None:
                    item.item = data.item
                if data.amount is not None:
                    item.amount = data.amount
                if data.details is not None:
                    item.details = data.details
                if data.price is not None:
                    item.price = data.price
                if data.unit is not None:
                    item.unit = data.unit
                item.timestamp_updated = datetime.datetime.now()
                await session.commit()
                await session.refresh(item)
            return item

    @staticmethod
    async def delete(item_id: str) -> bool:
        async with await get_session() as session:
            item = await session.get(OrderItem, item_id)
            if item:
                await session.delete(item)
                await session.commit()
                return True
            return False
