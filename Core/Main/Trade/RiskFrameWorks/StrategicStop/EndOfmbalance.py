from Core.Main.Asset.SubModels.Candle import Candle
from Interfaces.RiskManagement.IStrategicStop import IStrategicStop


class EndOfImbalance(IStrategicStop):
    def getStrategyStop(self, candle: Candle):
        if candle.close < candle.open:
            return candle.high
        if candle.close > candle.open:
            return candle.low
