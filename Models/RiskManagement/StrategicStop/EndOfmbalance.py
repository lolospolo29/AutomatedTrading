from Interfaces.RiskManagement.IStrategicStop import IStrategicStop
from Models.Main.Asset.Candle import Candle


class EndOfImbalance(IStrategicStop):
    def getStrategyStop(self, candle: Candle):
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
