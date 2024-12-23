from app.models.asset.Candle import Candle
from app.models.riskCalculations.entry.strategicStop.OBStopEnum import OrderBlockStop


class OBStop:
    @staticmethod
    def getStrategyStop(candle: Candle, mode: OrderBlockStop)->float:
        if mode == OrderBlockStop.WICK:
            if candle.close < candle.open:
                return candle.high
            if candle.close > candle.open:
                return candle.low
        if mode == OrderBlockStop.END:
            if candle.close < candle.open:
                return candle.open
            if candle.close > candle.open:
                return candle.close
        if mode == OrderBlockStop.FIFTY:
            fiftyPercent:float = (candle.open + candle.close) * 0.5
            return fiftyPercent
        return 0
