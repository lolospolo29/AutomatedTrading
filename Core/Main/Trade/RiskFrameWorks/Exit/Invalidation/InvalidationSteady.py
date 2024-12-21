from Core.Main.Asset.SubModels.Candle import Candle
from Core.Main.Trade.OrderDirectionEnum import OrderDirection


class InvalidationSteady:
    @staticmethod
    def checkInvalidation(stop: float, candle: Candle, direction: OrderDirection) ->bool:
        if direction == OrderDirection.BUY:
            if candle.low < stop:
                return True
            return False
        if direction == OrderDirection.SELL:
            if candle.high > stop:
                return True
            return False
