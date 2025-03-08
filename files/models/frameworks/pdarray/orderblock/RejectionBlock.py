from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray

class RejectionBlock:
    @staticmethod
    def detect_rejection_block(candle:Candle, average_range:float) -> PDArray:
                upper_wick = candle.high - max(candle.open, candle.close)
                lower_wick = min(candle.open, candle.close) - candle.low

                if  lower_wick > average_range:
                    return PDArray(name="RB",direction= "Bullish",candles=[candle],timeframe=candle.timeframe)
                elif upper_wick > average_range:
                    return PDArray(name="RB", direction="Bearish",candles=[candle],timeframe=candle.timeframe)