from enum import Enum


class PaymentMethod(str, Enum):
    CARD = "Картой"
    CASH = "Наличными"
    CRYPTO_INVOICE = "Крипто переводом"


class PaymentStatus(str, Enum):
    CREATED = "created"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class DeliveryMethod(str, Enum):
    SELF_PICKUP = "self_pickup"
    COURIER = "courier"
    PICKUP_POINT = "pickup_point"


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class OrderStatus(str, Enum):
    CREATED = "created"
    AWAITING_PAYMENT = "awaiting payment"
    READY_FOR_PICKUP = "ready for pickup"
    SHIPPED = "shipped"

    REVIEW = "user-rewiew"
    CANCELED = "canceled"
    RETURNED = "returned"
    REFUNDED = "refunded"
    FAILED = "failed"

    PACKED = "packed"
