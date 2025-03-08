from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray


class IFVG:
    @staticmethod
    def detect_ifvg(first_candle: Candle, second_candle: Candle, third_candle: Candle) -> PDArray:
        high1, low1 = first_candle.high, first_candle.low
        high2, low2, open2, close2 = second_candle.high, second_candle.low, second_candle.open, second_candle.close
        high3, low3 = third_candle.high, third_candle.low

        wick_high1 = high1 - max(first_candle.open, first_candle.close)
        wick_low1 = min(first_candle.open, first_candle.close) - low1
        wick_high3 = high3 - max(third_candle.open, third_candle.close)
        wick_low3 = min(third_candle.open, third_candle.close) - low3

        body2 = abs(open2 - close2)

        # Bullish IFVG: Large bullish candle with body overlapped by wicks of adjacent candles
        if close2 > open2 and body2 > max(wick_high1, wick_low1) and body2 > max(wick_high3, wick_low3):
            if low1 < high3:
                return PDArray(name="IFVG", direction='Bullish',
                               candles=[first_candle, second_candle, third_candle],
                               timeframe=first_candle.timeframe)

        # Bearish IFVG: Large bearish candle with body overlapped by wicks of adjacent candles
        if close2 < open2 and body2 > max(wick_high1, wick_low1) and body2 > max(wick_high3, wick_low3):
            if high1 > low3:
                return PDArray(name="IFVG", direction='Bearish',
                               candles=[first_candle, second_candle, third_candle],
                               timeframe=first_candle.timeframe)