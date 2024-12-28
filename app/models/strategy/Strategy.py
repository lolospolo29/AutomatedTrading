from typing import Tuple, Optional

from app.models.trade.Trade import Trade


class Strategy:
    def __init__(self,name: str,hasSMT: bool):
        self.name: str = name
        self.hasSMT: bool = hasSMT

    def returnExpectedTimeFrame(self):
        pass
    def getExit(self):
        pass
    def getEntry(self, candles: list, timeFrame: int, pd: list, level:list,
                 structure: list)-> Tuple[bool, Optional[Trade]]:
        pass
    def isInTime(self,time):
        pass
    def analyzeSMT(self):
        pass
    def analyzeData(self, candles: list, timeFrame: int) -> list:
        pass