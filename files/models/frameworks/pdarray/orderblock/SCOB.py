from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray


class SCOB:
    @staticmethod
    def detect_pd_single_candle_ob(first_candle:Candle, second_candle:Candle, third_candle) -> PDArray:

        high1 = first_candle.high
        high2 = second_candle.high
        low1 = first_candle.low
        low2 = second_candle.low
        close2 = second_candle.close
        close3 = third_candle.low

        if low2 < low1 < close2 and close3 > high2:
            return PDArray(name="SCOB", direction="Bullish", candles=[first_candle, second_candle, third_candle],
                              timeframe=first_candle.timeframe)
        if high2 > high1 > close2 and close3 < low2:
            return PDArray(name="SCOB", direction="Bearish", candles=[first_candle, second_candle, third_candle],
                              timeframe=first_candle.timeframe)