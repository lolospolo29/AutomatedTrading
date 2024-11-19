from Interfaces.RiskManagement.IStrategicStop import IStrategicStop
from Models.Main.Asset.Candle import Candle


class OBStop(IStrategicStop):
    def __init__(self, mode: str):
        self.mode: str = mode
    def getStrategyStop(self, candle: Candle):
        if self.mode == "Wick":
            if candle.close < candle.open:
                return candle.high
            if candle.close > candle.open:
                return candle.low
        if self.mode == "End":
            if candle.close < candle.open:
                return candle.open
            if candle.close > candle.open:
                return candle.close
        if self.mode == "50":
            return (candle.open + candle.close) * 0,5

