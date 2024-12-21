from Core.Main.Asset.SubModels.Candle import Candle


class DrillEntry:
    @staticmethod
    def getEntry(candle: Candle):
            return candle.close
