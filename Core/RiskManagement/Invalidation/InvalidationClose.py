from Core.Main.Asset.Candle import Candle
from Interfaces.RiskManagement.IRiskInvalidation import IRiskInvalidation


class InvalidationClose(IRiskInvalidation):
    def checkInvalidation(self, stopLoss: float, candle: Candle, tradeDirection: str) -> bool:
        if tradeDirection == 'long':
            if candle.close < stopLoss:
                return True
            return False
        if tradeDirection == 'short':
            if candle.close > stopLoss:
                return True
            return False

