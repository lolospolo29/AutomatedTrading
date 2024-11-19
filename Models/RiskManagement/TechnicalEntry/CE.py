from Interfaces.RiskManagement.ITechnicalEntry import ITechnicalEntry
from Models.Main.Asset.Candle import Candle


class CE(ITechnicalEntry):
    def getEntry(self, candle: Candle):
        return (candle.open + candle.close) * 0,5
