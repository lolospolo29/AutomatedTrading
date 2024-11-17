from Interfaces.RiskManagement.IRiskInvalidation import IRiskInvalidation
from Models.Main.Asset.Candle import Candle


class InvalidationSteady(IRiskInvalidation):
    def checkInvalidation(self, stopLoss: float, candle: Candle, tradeDirection: str):
        if tradeDirection == 'long':
            if candle.low < stopLoss:
                return True
            return False
        if tradeDirection == 'short':
            if candle.high > stopLoss:
                return True
            return False
