from enum import Enum


class PaymentType(str, Enum):
    CRYPTO_INVOICE = "crypto"
    CASH = "cash"


class PaymentStatus(str, Enum):
    NONE = "No payment method"

    # Invoice
    INVOICE_CREATED = "invoice created"
    INVOICE_SUBMITTED = "invoice submitted"
    INVOICE_APPROVED = "invoice approved"

    # Cash
    IN_CASH = "cash"

    # Finished
    PAYED = "payed"


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
