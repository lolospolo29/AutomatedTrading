from Core.Main.Asset.SubModels.Candle import Candle

class SwingStop:
    def getStrategyStop(self, candle: Candle):
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
