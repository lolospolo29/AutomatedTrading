from Core.Main.Asset.SubModels.Candle import Candle


class EndOfImbalance:
    @staticmethod
    def getStrategyStop(candle: Candle):
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
