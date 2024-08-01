from enum import Enum

class OrderStatus(str, Enum):
    CREATED = "created"
    USER_COMMENT = "user-comment"
    USER_REVIEW = "user-rewiew"
    PROCESSING = "processing"
    PACKED = "packed"
    COMPLETED = "completed"
    CANCELED = "canceled"
    RETURNED = "returned"
    REFUNDED = "refunded"
    FAILED = "failed"
