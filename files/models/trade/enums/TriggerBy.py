from enum import Enum


class TriggerBy(Enum):
    MARKPRICE = "MarkPrice"
    INDEXPRICE = "IndexPrice"
    LASTPRICE = "LastPrice"