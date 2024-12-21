from Core.Main.Asset.SubModels.Candle import Candle


class FillEntry:
    @staticmethod
    def getEntry(candle: Candle) -> float:
            return candle.open
