from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray

class IFVG:
    @staticmethod
    def return_pd_arrays(first_candle:Candle, second_candle:Candle, third_candle:Candle) -> PDArray:
        high1 = first_candle.high
        low1 = first_candle.low
        high2 = second_candle.high
        low2 = second_candle.low
        high3 = third_candle.high
        low3 = third_candle.low
        open2 = second_candle.open
        close2 = second_candle.close

        wick_high = high2 - max(open2, close2)
        wick_low = min(open2, close2) - low2
        body = abs(open2-close2)
        if high1 < low3 and (body > wick_high or body > wick_low):
            return PDArray(name="IFVG", direction='Bullish',
                           candles=[first_candle, second_candle, third_candle],
                           timeframe=first_candle.timeframe)

        if low1 < high3 and (body > wick_high or body > wick_low):
            return PDArray(name="IFVG", direction='Bearish',
                           candles=[first_candle, second_candle, third_candle],
                           timeframe=first_candle.timeframe)