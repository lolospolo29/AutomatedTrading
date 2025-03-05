from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray


class BPR:
    @staticmethod
    def detect_bpr(buy_fvg:PDArray, sell_fvg:PDArray) -> PDArray:

        buy_fvg.candles.sort(key=lambda x: x.iso_time)
        sell_fvg.candles.sort(key=lambda x: x.iso_time)

        last_candle_buy_fvg: Candle = buy_fvg.candles[-1]
        last_candle_sell_fvg: Candle = sell_fvg.candles[-1]

        # Nutze Generatoren für min/max
        sell_fvg_low = min(candle.low for candle in sell_fvg.candles)
        buy_fvg_low = min(candle.low for candle in buy_fvg.candles)

        sell_fvg_high = max(candle.high for candle in sell_fvg.candles)
        buy_fvg_high = max(candle.high for candle in buy_fvg.candles)

        # Berechne Overlap
        overlapLow = max(sell_fvg_low, buy_fvg_low)
        overlapHigh = min(sell_fvg_high, buy_fvg_high)

        if overlapLow < overlapHigh:
            # There is an overlap, create a Balanced Price Range (BPR)

            # Determine the direction based on the order of the FVGs
            direction = "Bullish"  # Default direction is bullish

            # If the first FVG (sell_fvg) is Bearish and the second (buy_fvg) is Bullish
            if last_candle_sell_fvg.iso_time < last_candle_buy_fvg.iso_time:
                direction = "Bullish"
            # If the first FVG (buy_fvg) is Bullish and the second (sell_fvg) is Bearish
            if last_candle_sell_fvg.iso_time > last_candle_buy_fvg.iso_time:
                direction = "Bearish"

            candles = []
            candles.extend(buy_fvg.candles)
            candles.extend(sell_fvg.candles)

            return PDArray(name="BPR", direction=direction, candles=candles,
                              timeframe=last_candle_buy_fvg.timeframe)