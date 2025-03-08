from enum import Enum


class OrderBlockStatusEnum(Enum):
    Normal = "Normal"
    Breaker = "Breaker"
    Reclaimed = "Reclaimed"