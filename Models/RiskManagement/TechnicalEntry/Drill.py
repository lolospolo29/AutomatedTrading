from Interfaces.RiskManagement.ITechnicalEntry import ITechnicalEntry
from Models.Main.Asset.Candle import Candle


class DrillEntry(ITechnicalEntry):
    def getEntry(self, candle: Candle):
            return candle.close
