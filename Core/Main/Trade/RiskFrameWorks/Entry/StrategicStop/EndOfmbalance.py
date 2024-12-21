from Core.Main.Asset.SubModels.Candle import Candle


class EndOfImbalance:
    @staticmethod
    def getStrategyStop(candle: Candle) -> float:
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
        return 0
