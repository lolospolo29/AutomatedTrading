from Core.Main.Asset.Candle import Candle
from Interfaces.RiskManagement.ITechnicalEntry import ITechnicalEntry


class DrillEntry(ITechnicalEntry):
    def getEntry(self, candle: Candle):
            return candle.close