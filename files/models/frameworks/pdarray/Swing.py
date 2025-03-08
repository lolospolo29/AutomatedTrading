from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray

class Swing:

    @staticmethod
    def detect_swing(first_candle:Candle, second_candle:Candle, third_candle:Candle) -> PDArray:
        high1 = first_candle.high
        high2 = second_candle.high
        high3 = third_candle.high
        low1 = first_candle.low
        low2 = second_candle.low
        low3 = third_candle.low

        if high3 < high2 and high1 < high2:
            return PDArray(name="High", direction="Bullish",
                               candles=[first_candle, second_candle, third_candle],
                               timeframe=first_candle.timeframe)
        if low3 > low2 and low1 > low2:
            return PDArray(name="Low", direction="Bearish",
                               candles=[first_candle,second_candle,third_candle],
                               timeframe=first_candle.timeframe)

    @staticmethod
    def detect_sweep(last_candle:Candle, swing:PDArray) -> bool:
        if swing.status == "Sweeped":
            return True
        if swing.direction == "Bullish":
            highest_candle = max(candle.high for candle in swing.candles)
            if highest_candle < last_candle.high:
                return True
        if swing.direction == "Bearish":
            lowest_candle = min(candle.low for candle in swing.candles)
            if lowest_candle > last_candle.low:
                return True
        return False