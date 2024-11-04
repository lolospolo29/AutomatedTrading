from Interfaces.RiskManagement.IRatio import IRatio


class FixedRatio(IRatio):
    def __init__(self, ratio):
        self.ratio = ratio

    def getRatio(self, stop, takeProfit):
        pass

    def isRatioValid(self, stop, takeProfit):
        pass
