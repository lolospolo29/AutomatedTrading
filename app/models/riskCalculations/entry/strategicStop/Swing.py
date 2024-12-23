from app.models.asset.Candle import Candle


class SwingStop:
    @staticmethod
    def getStrategyStop(candle: Candle):
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
        return 0
