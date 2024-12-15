from Core.Main.Asset.SubModels.Candle import Candle
from Interfaces.RiskManagement.ITechnicalEntry import ITechnicalEntry


class CE(ITechnicalEntry):
    def getEntry(self, candle: Candle):
        return (candle.open + candle.close) * 0,5
