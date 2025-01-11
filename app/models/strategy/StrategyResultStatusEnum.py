from enum import Enum


class StrategyResultStatusEnum(Enum):
    NEWORDER = "New Order"
    AMENDORDER = "Amend Order"
    CANCELL = "Cancel Order"
    NONEW = "No New Found"