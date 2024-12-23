from app.models.asset.Candle import Candle


class CE:
    @staticmethod
    def getEntry(candle: Candle) -> float:
        return (candle.open + candle.close) * 0.5

