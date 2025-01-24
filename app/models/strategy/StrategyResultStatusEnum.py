from enum import Enum


class StrategyResultStatusEnum(Enum):
    NEWTRADE = "New Trade"
    NEWORDER = "New Order"
    AMENDORDER = "Amend Order"
    CANCELL = "Cancel Order"
    NONEW = "No New Found"