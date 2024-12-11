from Core.Main.Asset.Candle import Candle
from Interfaces.RiskManagement.IStrategicStop import IStrategicStop


class OBStop(IStrategicStop):
    def getStrategyStop(self, candle: Candle,mode: str):
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
            return (candle.open + candle.close) * 0,5

