# server/crud.py
from sqlmodel import select
from typing import Optional
from .models import User, Order
from .schemas import UserCreate, UserUpdate, OrderCreate, OrderUpdate
from .db_config import get_session
import datetime

# CRUD operations for User
async def create_user(user: UserCreate) -> User:
    async with await get_session() as session:
        user_obj = User(name=user.name, telegram_id=user.telegram_id)
        session.add(user_obj)
        await session.commit()
        await session.refresh(user_obj)
        return user_obj

async def get_user(user_id: str) -> Optional[User]:
    async with await get_session() as session:
        user = await session.get(User, user_id)
        return user
    
async def get_user_by_telegram_id(telegram_id: str) -> Optional[User]:
    async with await get_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

async def get_users() -> list[User]:
    async with await get_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

async def update_user(user_id: str, user_update: UserUpdate) -> Optional[User]:
    async with await get_session() as session:
        user = await session.get(User, user_id)
        if user:
            if user_update.name is not None:
                user.name = user_update.name
            if user_update.telegram_id is not None:
                user.telegram_id = user_update.telegram_id
            user.timestamp_updated = datetime.datetime.now()
            await session.commit()
            await session.refresh(user)
        return user

async def delete_user(user_id: str) -> bool:
    async with await get_session() as session:
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False

# CRUD operations for Order
async def create_order(order: OrderCreate) -> Order:
    async with await get_session() as session:
        order_obj = Order(items=order.items, price=order.price, user=order.user, comment=order.comment)
        session.add(order_obj)
        await session.commit()
        await session.refresh(order_obj)
        return order_obj

async def get_order(order_id: str) -> Optional[Order]:
    async with await get_session() as session:
        order = await session.get(Order, order_id)
        return order

async def get_orders() -> list[Order]:
    async with await get_session() as session:
        result = await session.execute(select(Order))
        return result.scalars().all()

async def get_orders_by_user(user_id: str) -> list[Order]:
    async with await get_session() as session:
        result = await session.execute(select(Order).where(Order.user == user_id))
        return result.scalars().all()

async def update_order(order_id: str, order_update: OrderUpdate) -> Optional[Order]:
    async with await get_session() as session:
        order = await session.get(Order, order_id)
        if order:
            if order_update.review is not None:
                order.review = order_update.review
            if order_update.comment is not None:
                order.comment = order_update.comment
            if order_update.is_delivered is not None:
                order.is_delivered = order_update.is_delivered
            if order_update.is_paid is not None:
                order.is_paid = order_update.is_paid
            if order_update.price is not None:
                order.price = order_update.price
            if order_update.status is not None:
                order.status = order_update.status
            order.timestamp_updated = datetime.datetime.now()
            await session.commit()
            await session.refresh(order)
        return order

async def delete_order(order_id: str) -> bool:
    async with await get_session() as session:
        order = await session.get(Order, order_id)
        if order:
            await session.delete(order)
            await session.commit()
            return True
        return False
