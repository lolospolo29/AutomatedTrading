from enum import Enum

class TimeInForce(Enum):
    IOC = "IOC"
    GTC = "GTC"
    FOK = "FOK"
    GTD = "GTD"