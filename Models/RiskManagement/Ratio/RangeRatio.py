from Interfaces.RiskManagement.IRatio import IRatio


class RangeRatio(IRatio):
    def __init__(self, range):
        self.range = range

    def getRatio(self, stop, takeProfit):
        pass

    def isRatioValid(self):
        return True
