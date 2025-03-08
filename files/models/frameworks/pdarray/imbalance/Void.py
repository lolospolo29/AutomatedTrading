from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray


class Void:
    @staticmethod
    def detect_void(first_candle:Candle, second_candle:Candle) -> PDArray:
        if second_candle.low > first_candle.high:
            return PDArray(name="LV", direction="Bullish", candles=[first_candle, second_candle],
                               timeframe=first_candle.timeframe)
        elif second_candle.high < first_candle.low:
            return PDArray(name="LV", direction="Bearish", candles=[first_candle, second_candle],
                               timeframe=first_candle.timeframe)