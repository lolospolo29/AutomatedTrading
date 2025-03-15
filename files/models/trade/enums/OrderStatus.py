from enum import Enum


class OrderStatus(Enum):
    NEW = "New"
    PARTIALLYFILLED = "PartiallyFilled"
    UNTRIGGERED = "Untriggered"
    REJECTED = "Rejected"
    PARTIALLYFILLEDCANCELLED = "PartiallyFilledCancelled"
    FILLED = "Filled"
    CANCELLED = "Cancelled"
    TRIGGERED = "Triggered"
    DEACTIVATED = "Deactivated"