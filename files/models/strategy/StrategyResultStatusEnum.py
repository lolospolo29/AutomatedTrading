from enum import Enum


class StrategyResultStatusEnum(Enum):
    NEWTRADE = "New Trade"
    CHANGED = "Changed Trade"
    CLOSE = "Close Trade"
    NOCHANGE = "No Change"