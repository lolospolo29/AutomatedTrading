from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray


class PB:
    @staticmethod
    def return_pd_arrays(last_candle: Candle, orderblock: PDArray) -> PDArray:
        if orderblock.direction == "Bullish":
            # Find last bearish candle with the lowest close
            last_bearish_candles = [candle for candle in orderblock.candles if candle.close < candle.open]
            if last_bearish_candles:
                last_bearish_candle = min(last_bearish_candles, key=lambda c: c.close)
                # Check if last candle is bearish and within the range
                if last_candle.close < last_candle.open and last_bearish_candle.low < last_candle.low < last_candle.high:
                    return PDArray(name="PB", direction="Bullish", candles=[last_candle],
                                   timeframe=last_candle.timeframe, reference_pd=orderblock.id)

        if orderblock.direction == "Bearish":
            # Find last bullish candle with the highest close
            last_bullish_candles = [candle for candle in orderblock.candles if candle.close > candle.open]
            if last_bullish_candles:
                last_bullish_candle = max(last_bullish_candles, key=lambda c: c.close)
                # Check if last candle is bullish and within the range
                if last_candle.close > last_candle.open and last_bullish_candle.low < last_candle.high < last_bullish_candle.high:
                    return PDArray(name="OB", direction="Bearish", candles=[last_candle],
                                   timeframe=last_candle.timeframe, reference_pd=orderblock.id)