from enum import Enum


class TriggerByEnum(Enum):
    MARKPRICE = "MarkPrice"
    INDEXPRICE = "IndexPrice"
    LASTPRICE = "LastPrice"