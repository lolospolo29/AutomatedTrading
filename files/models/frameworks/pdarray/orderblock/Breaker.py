from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.pdarray.orderblock.OrderBlockStatusEnum import OrderBlockStatusEnum


class Breaker:
    @staticmethod
    def detect_breaker(last_candle:Candle, orderblock:PDArray) -> bool:
        if orderblock.status != OrderBlockStatusEnum.Breaker.value:
            if orderblock.direction == "Bullish":
                lowest_candle = min(orderblock.candles, key=lambda candle: candle.low)
                if last_candle.close < lowest_candle.low:
                    return True
            if orderblock.direction == "Bearish":
                highest_candle = max(orderblock.candles, key=lambda candle: candle.high)
                if last_candle.close > highest_candle.high:
                    return True
        return False