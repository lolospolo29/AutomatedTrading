from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray

class VolumeImbalance:
    @staticmethod
    def detect_volume_imbalance(first_candle:Candle, second_candle:Candle) -> PDArray:
        if min(second_candle.open, second_candle.close) > first_candle.high and \
                second_candle.low > max(first_candle.open, first_candle.close) and \
                (second_candle.low <= first_candle.high):
            return PDArray(name="VI", direction="Bullish", candles=[first_candle, second_candle],
                               timeframe=first_candle.timeframe)
        elif max(second_candle.open, second_candle.close) < second_candle.low and \
                second_candle.high < min(first_candle.open, first_candle.close) and \
                (second_candle.high >= first_candle.low):
            return PDArray(name="VI", direction="Bearish", candles=[first_candle, second_candle],
                               timeframe=first_candle.timeframe)