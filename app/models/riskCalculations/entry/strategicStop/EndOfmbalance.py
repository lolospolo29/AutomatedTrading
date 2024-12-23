from app.models.asset.Candle import Candle


class EndOfImbalance:
    @staticmethod
    def getStrategyStop(candle: Candle) -> float:
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
        return 0
