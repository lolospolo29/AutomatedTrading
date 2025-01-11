from app.models.asset.Candle import Candle
from app.models.trade.enums.OrderDirectionEnum import OrderDirection


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
