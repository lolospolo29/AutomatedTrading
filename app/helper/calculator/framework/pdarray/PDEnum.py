from enum import Enum


class PDEnum(Enum):
    BPR = "BPR"
    BREAKER = "BRK"
    FVG = "FVG"
    OrderBlock = "OB"
    RejectionBlock = "RB"
    SWINGS = "Swings"
    VOID = "VOID"
    VOLUMEIMBALANCE = "VI"