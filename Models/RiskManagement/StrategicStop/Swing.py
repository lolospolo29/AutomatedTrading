from Interfaces.RiskManagement.IStrategicStop import IStrategicStop
from Models.Main.Asset.Candle import Candle


class SwingStop(IStrategicStop):
    def getStrategyStop(self, candle: Candle):
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
