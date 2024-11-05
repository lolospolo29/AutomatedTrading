from Interfaces.Strategy.IStrategy import IStrategy


class Strategy(IStrategy):
    def __init__(self,name):
        self.name = name

    def getExit(self):
        pass

    def getEntry(self):
        pass

    def isInTime(self):
        pass

    def analyzeCurrentData(self, data_points):
        pass

    def analyzePreviousData(self):
        pass