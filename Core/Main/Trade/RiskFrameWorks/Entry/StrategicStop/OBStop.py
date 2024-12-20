from Core.Main.Asset.SubModels.Candle import Candle


class OBStop:
    @staticmethod
    def getStrategyStop(candle: Candle, mode: str)->float:
        if mode == "Wick":
            if candle.close < candle.open:
                return candle.high
            if candle.close > candle.open:
                return candle.low
        if mode == "End":
            if candle.close < candle.open:
                return candle.open
            if candle.close > candle.open:
                return candle.close
        if mode == "50":
            fiftyPercent:float = (candle.open + candle.close) * 0.5
            return fiftyPercent

