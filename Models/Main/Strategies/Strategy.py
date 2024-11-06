from Interfaces.Strategy.IStrategy import IStrategy


class Strategy(IStrategy):
    def __init__(self,name):
        self.name = name
    def returnExpectedTimeFrame(self):
        pass
    def getExit(self):
        pass
    def getEntry(self):
        pass
    def isInTime(self):
        pass
    def analyzeData(self):
        pass