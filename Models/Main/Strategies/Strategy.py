from Interfaces.Strategy.IStrategy import IStrategy


class Strategy(IStrategy):
    def __init__(self,name: str,hasSMT: bool,dataDuration: int):
        self.name: str = name
        self.hasSMT: bool = hasSMT
        self.dataDuration: int = dataDuration # Days to Save Data in DB and required for Strategy
    def returnExpectedTimeFrame(self):
        pass
    def returnDataDuration(self):
        return self.dataDuration
    def getExit(self):
        pass
    def getEntry(self, candles: list, timeFrame: int, pd: list, level:list, structure: list):
        pass
    def isInTime(self,time):
        pass
    def analyzeSMT(self):
        pass
    def analyzeData(self, candles: list, timeFrame: int) -> list:
        pass