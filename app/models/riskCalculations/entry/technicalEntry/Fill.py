from app.models.asset.Candle import Candle


class FillEntry:
    @staticmethod
    def getEntry(candle: Candle) -> float:
            return candle.open
