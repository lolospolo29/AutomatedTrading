from enum import Enum


class OrderStatusEnum(Enum):
    PENDING = "pending"
    CLOSED = "closed"
    ACTIVE = "active"
    CREATED = "created"