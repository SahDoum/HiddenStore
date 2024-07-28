from pydantic import BaseModel
from typing import Optional
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"

class UserCreate(BaseModel):
    name: str
    telegram_id: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    telegram_id: Optional[str] = None

class OrderCreate(BaseModel):
    items: list[dict[str, str]]
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
