# server/api.py
from typing import Optional
import datetime
from sqlmodel import select

from libs.models.models import (
    User,
    Order,
    OrderItem,
    DeliveryDetails,
    PaymentIntent,
    PickupPoint,
    TimeSlot,
)
from libs.models.schemas import (
    UserCreate,
    UserUpdate,
    OrderCreate,
    OrderUpdate,
    OrderItemCreate,
    OrderItemUpdate,
    DeliveryDetailsCreate,
    DeliveryDetailsUpdate,
    PaymentIntentCreate,
    PaymentIntentUpdate,
    PickupPointCreate,
    PickupPointUpdate,
    TimeSlotCreate,
    TimeSlotUpdate,
)

from libs.models.statuses import PaymentMethod, DeliveryMethod

from db_config import get_session


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
            result = await session.execute(
                select(User).order_by(User.timestamp_created.desc())
            )
            return list(result.scalars().all())

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

            # create payment
            # create delivery

            payment_method = (
                data.payment_method if data.payment_method else PaymentMethod.CASH
            )

            payment = PaymentIntent(
                amount=data.price, method=payment_method, payment_details={}
            )
            session.add(payment)
            await session.commit()
            await session.refresh(payment)

            delivery = DeliveryDetails(
                method=DeliveryMethod.PICKUP_POINT, pickup_point_id=data.pickup_point_id
            )
            session.add(delivery)
            await session.commit()
            await session.refresh(delivery)

            order = Order(
                items=data.items,
                price=data.price,
                user=data.user,
                comment=data.comment,
                payment_id=payment.id,
                delivery_id=delivery.id,
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
            result = await session.execute(
                select(Order).order_by(Order.timestamp_created.desc())
            )
            return list(result.scalars().all())

    @staticmethod
    async def get_by_user(user_id: str) -> list[Order]:
        async with await get_session() as session:
            result = await session.execute(select(Order).where(Order.user == user_id))
            return list(result.scalars().all())

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
            result = await session.execute(
                select(OrderItem).order_by(OrderItem.timestamp_created.desc())
            )
            return list(result.scalars().all())

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


class PickupPointAPI:
    @staticmethod
    async def create(data: PickupPointCreate) -> PickupPoint:
        async with await get_session() as session:
            pickuppoint = PickupPoint(
                address=data.address, description=data.description
            )
            session.add(pickuppoint)
            await session.commit()
            await session.refresh(pickuppoint)
            return pickuppoint

    @staticmethod
    async def get(pickuppoint_id: str) -> Optional[PickupPoint]:
        async with await get_session() as session:
            return await session.get(PickupPoint, pickuppoint_id)

    @staticmethod
    async def get_all() -> list[PickupPoint]:
        async with await get_session() as session:
            result = await session.execute(
                select(PickupPoint).order_by(PickupPoint.timestamp_created.desc())
            )
            return list(result.scalars().all())

    @staticmethod
    async def update(
        pickuppoint_id: str, data: PickupPointUpdate
    ) -> Optional[PickupPoint]:
        async with await get_session() as session:
            pickuppoint = await session.get(PickupPoint, pickuppoint_id)
            if pickuppoint:
                if data.address is not None:
                    pickuppoint.address = data.address
                if data.description is not None:
                    pickuppoint.description = data.description
                pickuppoint.timestamp_updated = datetime.datetime.now()
                await session.commit()
                await session.refresh(pickuppoint)
            return pickuppoint

    @staticmethod
    async def delete(pickuppoint_id: str) -> bool:
        async with await get_session() as session:
            pickuppoint = await session.get(PickupPoint, pickuppoint_id)
            if pickuppoint:
                await session.delete(pickuppoint)
                await session.commit()
                return True
            return False


class PaymentIntentAPI:
    @staticmethod
    async def create(data: PaymentIntentCreate) -> PaymentIntent:
        async with await get_session() as session:
            payment_intent = PaymentIntent(
                amount=data.amount,
                method=data.method,
                payment_details=data.payment_details,
            )
            session.add(payment_intent)
            await session.commit()
            await session.refresh(payment_intent)
            return payment_intent

    @staticmethod
    async def get(payment_intent_id: str) -> Optional[PaymentIntent]:
        async with await get_session() as session:
            return await session.get(PaymentIntent, payment_intent_id)

    @staticmethod
    async def get_all() -> list[PaymentIntent]:
        async with await get_session() as session:
            result = await session.execute(
                select(PaymentIntent).order_by(PaymentIntent.timestamp_created.desc())
            )
            return list(result.scalars().all())

    @staticmethod
    async def update(
        payment_intent_id: str, data: PaymentIntentUpdate
    ) -> Optional[PaymentIntent]:
        async with await get_session() as session:
            payment_intent = await session.get(PaymentIntent, payment_intent_id)
            if payment_intent:
                if data.status is not None:
                    payment_intent.status = data.status
                if data.payment_details is not None:
                    payment_intent.payment_details = data.payment_details
                payment_intent.timestamp_updated = datetime.datetime.now()
                await session.commit()
                await session.refresh(payment_intent)
            return payment_intent

    @staticmethod
    async def delete(payment_intent_id: str) -> bool:
        async with await get_session() as session:
            payment_intent = await session.get(PaymentIntent, payment_intent_id)
            if payment_intent:
                await session.delete(payment_intent)
                await session.commit()
                return True
            return False


class DeliveryDetailsAPI:
    @staticmethod
    async def create(data: DeliveryDetailsCreate) -> DeliveryDetails:
        async with await get_session() as session:
            delivery_details = DeliveryDetails(
                method=data.method,
                address=data.address,
                pickup_point_id=data.pickup_point_id,
                delivery_time=data.delivery_time,
                courier_id=data.courier_id,
                additional_info=data.additional_info,
            )
            session.add(delivery_details)
            await session.commit()
            await session.refresh(delivery_details)
            return delivery_details

    @staticmethod
    async def get(delivery_details_id: str) -> Optional[DeliveryDetails]:
        async with await get_session() as session:
            return await session.get(DeliveryDetails, delivery_details_id)

    @staticmethod
    async def get_all() -> list[DeliveryDetails]:
        async with await get_session() as session:
            result = await session.execute(
                select(DeliveryDetails).order_by(
                    DeliveryDetails.timestamp_created.desc()
                )
            )
            return list(result.scalars().all())

    @staticmethod
    async def update(
        delivery_details_id: str, data: DeliveryDetailsUpdate
    ) -> Optional[DeliveryDetails]:
        async with await get_session() as session:
            delivery_details = await session.get(DeliveryDetails, delivery_details_id)
            if delivery_details:
                if data.status is not None:
                    delivery_details.status = data.status
                if data.address is not None:
                    delivery_details.address = data.address
                if data.delivery_time is not None:
                    delivery_details.delivery_time = data.delivery_time
                if data.courier_id is not None:
                    delivery_details.courier_id = data.courier_id
                if data.additional_info is not None:
                    delivery_details.additional_info = data.additional_info
                delivery_details.timestamp_updated = datetime.datetime.now()
                await session.commit()
                await session.refresh(delivery_details)
            return delivery_details

    @staticmethod
    async def delete(delivery_details_id: str) -> bool:
        async with await get_session() as session:
            delivery_details = await session.get(DeliveryDetails, delivery_details_id)
            if delivery_details:
                await session.delete(delivery_details)
                await session.commit()
                return True
            return False


class TimeSlotsAPI:
    @staticmethod
    async def create(data: TimeSlotCreate) -> TimeSlot:
        async with await get_session() as session:
            # Проверим, что новый слот не пересекается с уже существующими
            conflicting_slots = await session.execute(
                select(TimeSlot)
                .where(TimeSlot.date == data.date)
                .where(TimeSlot.start_time < data.end_time)
                .where(TimeSlot.end_time > data.start_time)
            )
            if conflicting_slots.scalars().first():
                raise ValueError(
                    "Новый слот пересекается с существующими временными интервалами"
                )

            new_slot = TimeSlot(
                date=data.date, start_time=data.start_time, end_time=data.end_time
            )
            session.add(new_slot)
            await session.commit()
            await session.refresh(new_slot)
            return new_slot

    @staticmethod
    async def get(slot_id: str) -> Optional[TimeSlot]:
        async with await get_session() as session:
            return await session.get(TimeSlot, slot_id)

    @staticmethod
    async def get_all() -> list[TimeSlot]:
        async with await get_session() as session:
            result = await session.execute(
                select(TimeSlot).order_by(TimeSlot.date.desc(), TimeSlot.start_time)
            )
            return list(result.scalars().all())

    @staticmethod
    async def get_by_date(date: datetime.date) -> list[TimeSlot]:
        async with await get_session() as session:
            result = await session.execute(
                select(TimeSlot).where(TimeSlot.date == date)
            )
            return list(result.scalars().all())

    @staticmethod
    async def update(slot_id: str, data: TimeSlotUpdate) -> Optional[TimeSlot]:
        async with await get_session() as session:
            slot = await session.get(TimeSlot, slot_id)
            if slot:
                if data.start_time is not None:
                    slot.start_time = data.start_time
                if data.end_time is not None:
                    slot.end_time = data.end_time
                if data.date is not None:
                    slot.date = data.date

                # Проверим, что обновленный слот не пересекается с существующими
                conflicting_slots = await session.execute(
                    select(TimeSlot)
                    .where(TimeSlot.id != slot_id)  # Исключаем текущий слот
                    .where(TimeSlot.date == slot.date)
                    .where(TimeSlot.start_time < slot.end_time)
                    .where(TimeSlot.end_time > slot.start_time)
                )
                if conflicting_slots.scalars().first():
                    raise ValueError(
                        "Обновленный слот пересекается с существующими временными интервалами"
                    )

                slot.timestamp_updated = datetime.datetime.now()
                await session.commit()
                await session.refresh(slot)
            return slot

    @staticmethod
    async def delete(slot_id: str) -> bool:
        async with await get_session() as session:
            slot = await session.get(TimeSlot, slot_id)
            if slot:
                await session.delete(slot)
                await session.commit()
                return True
            return False
