from app.models.asset.Candle import Candle
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum


class InvalidationSteady:
    """Stop Loss Check"""
    @staticmethod
    def check_invalidation(stop: float, candle: Candle, direction: OrderDirectionEnum) ->bool:
        if direction == OrderDirectionEnum.BUY:
            if candle.low < stop:
                return True
            return False
        if direction == OrderDirectionEnum.SELL:
            if candle.high > stop:
                return True
            return False
