from app.models.asset.Candle import Candle


class DrillEntry:
    @staticmethod
    def getEntry(candle: Candle):
            return candle.close
