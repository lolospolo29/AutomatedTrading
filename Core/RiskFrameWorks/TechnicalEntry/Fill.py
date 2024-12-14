from Interfaces.RiskManagement.ITechnicalEntry import ITechnicalEntry


class FillEntry(ITechnicalEntry):
    def getEntry(self, candle):
            return candle.open
