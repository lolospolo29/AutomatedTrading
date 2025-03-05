from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray

class Orderblock:
    @staticmethod
    def return_orderblock(first_candle:Candle, second_candle:Candle) -> PDArray:

        open1 = first_candle.open
        open2 = second_candle.open
        high1 = first_candle.high
        high2 = second_candle.high
        low1 = first_candle.low
        low2 = second_candle.low
        close1 = first_candle.close
        close2 = second_candle.close

        if close1 < open1 and close2 > open2 and close2 > high1 and low1 > low2:
            return PDArray(name="OB", direction="Bullish", candles=[first_candle, second_candle],
                              timeframe=first_candle.timeframe)
        if close1 > open1 and close2 < open2 and close2 < low1 and high1 < high2:
           return PDArray(name="OB", direction="Bearish", candles=[first_candle, second_candle],
                              timeframe=first_candle.timeframe)