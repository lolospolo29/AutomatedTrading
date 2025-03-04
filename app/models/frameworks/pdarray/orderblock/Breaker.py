from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray

class Breaker:
    @staticmethod
    def return_pd_arrays(last_candle:Candle, orderblock:PDArray) -> bool:
        if orderblock.status != "Breaker":
            if orderblock.direction == "Bullish":
                lowest_candle = min(orderblock.candles, key=lambda candle: candle.low)
                if last_candle.close < lowest_candle.low:
                    return True
            if orderblock.direction == "Bearish":
                highest_candle = max(orderblock.candles, key=lambda candle: candle.high)
                if last_candle.close > highest_candle.high:
                    return True
        return False