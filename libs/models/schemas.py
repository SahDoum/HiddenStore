from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
import datetime

from .statuses import (
    OrderStatus,
    PaymentMethod,
    PaymentStatus,
    DeliveryMethod,
    DeliveryStatus,
)


class UserCreate(BaseModel):
    name: str
    telegram_id: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    telegram_id: Optional[str] = None


class OrderCreate(BaseModel):
    items: list[tuple[str, float]]
    price: int
    user: str
    comment: Optional[str] = None
    pickup_point_id: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None


class OrderUpdate(BaseModel):
    review: Optional[str] = None
    comment: Optional[str] = None
    is_delivered: Optional[bool] = None
    is_paid: Optional[bool] = None
    price: Optional[int] = None
    status: Optional[OrderStatus] = None


class OrderItemCreate(BaseModel):
    item: str
    amount: Optional[int] = None
    details: Optional[str] = None
    price: int
    unit: str


class OrderItemUpdate(BaseModel):
    item: Optional[str] = None
    amount: Optional[int] = None
    details: Optional[str] = None
    price: Optional[int] = None
    unit: Optional[str] = None


class PickupPointCreate(BaseModel):
    address: Optional[str]
    description: Optional[str]


class PickupPointUpdate(BaseModel):
    address: Optional[str] = None
    description: Optional[str] = None


class PaymentIntentCreate(BaseModel):
    amount: int
    method: PaymentMethod
    payment_details: Optional[dict] = None


class PaymentIntentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    payment_details: Optional[dict] = None


class DeliveryDetailsCreate(BaseModel):
    method: DeliveryMethod
    address: Optional[str] = None
    pickup_point_id: Optional[str] = None
    delivery_time: Optional[datetime.datetime] = None
    courier_id: Optional[str] = None
    additional_info: Optional[str] = None


class DeliveryDetailsUpdate(BaseModel):
    status: Optional[DeliveryStatus] = None
    address: Optional[str] = None
    delivery_time: Optional[datetime.datetime] = None
    courier_id: Optional[str] = None
    additional_info: Optional[str] = None


class TimeSlotCreate(BaseModel):
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time

    @field_validator("end_time")
    def validate_time(cls, end_time, values):
        start_time = values.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("Время окончания должно быть позже времени начала")
        return end_time


class TimeSlotUpdate(BaseModel):
    date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None

    @model_validator(mode="before")
    def check_times(cls, values):
        start_time = values.get("start_time")
        end_time = values.get("end_time")

        if start_time and end_time:
            if end_time <= start_time:
                raise ValueError("Время окончания должно быть позже времени начала")
        return values

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError("Необходимо передать хотя бы одно поле для обновления")
        return values
