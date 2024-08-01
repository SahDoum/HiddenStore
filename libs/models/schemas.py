from pydantic import BaseModel
from typing import Optional
from .models import OrderStatus, OrderItem

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
