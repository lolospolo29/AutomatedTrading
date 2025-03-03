from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray

class RejectionBlock:
    @staticmethod
    def return_pd_arrays(candle:Candle, average_range:float) -> PDArray:
                # Calculate the wicks
                upper_wick = candle.high - max(candle.open, candle.close)
                lower_wick = min(candle.open, candle.close) - candle.low

                # Bullish rejection: Large lower wick compared to average range
                if  lower_wick > average_range:
                    return PDArray(name="RB",direction= "Bullish",candles=[candle],timeframe=candle.timeframe)
                elif upper_wick > average_range:
                    return PDArray(name="RB", direction="Bearish",candles=[candle],timeframe=candle.timeframe)