from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray


class FVG:
    @staticmethod
    def return_pd_arrays(first_candle:Candle, second_candle:Candle, third_candle:Candle) -> PDArray:
        if first_candle.low > third_candle.high and second_candle.close < first_candle.low:
            return PDArray(name="FVG", direction='Bearish',
                           candles=[first_candle, second_candle, third_candle],
                           timeframe=first_candle.timeframe)
        elif first_candle.high < third_candle.low and second_candle.close > first_candle.high:
            return PDArray(name="FVG", direction='Bullish',
                              candles=[first_candle, second_candle, third_candle],
                              timeframe=first_candle.timeframe)