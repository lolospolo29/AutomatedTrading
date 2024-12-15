from Core.Main.Asset.SubModels.Candle import Candle


class InvalidationClose:

    @staticmethod
    def checkInvalidation(stop: float, candle: Candle, direction: str) -> bool:
        if direction == 'Buy':
            if candle.close < stop:
                return True
            return False
        if direction == 'Sell':
            if candle.close > stop:
                return True
            return False

