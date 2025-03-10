from enum import Enum


class PDEnum(Enum):
    BPR = "BPR"
    BREAKER = "BRK"
    FVG = "FVG"
    IFVG = "IFVG"
    OrderBlock = "OB"
    RejectionBlock = "RB"
    SWINGS = "Swings"
    VOID = "VOID"
    VOLUMEIMBALANCE = "VI"
    SCOB = "SCOB"