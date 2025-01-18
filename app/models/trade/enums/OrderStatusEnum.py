from enum import Enum


class OrderStatusEnum(Enum):
    NEW = "New"
    PARTIALLYFILLED = "PartiallyFilled"
    UNTRIGGERED = "Untriggered"
    REJECTED = "Rejected"
    PARTIALLYFILLEDCANCELLED = "PartiallyFilledCancelled"
    FILLED = "Filled"
    CANCELLED = "Cancelled"
    TRIGGERED = "Triggered"
    DEACTIVATED = "Deactivated"