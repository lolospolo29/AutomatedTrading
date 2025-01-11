from enum import Enum

class TimeInForceEnum(Enum):
    IOC = "IOC"
    GTC = "GTC"
    FOK = "FOK"
    GTD = "GTD"