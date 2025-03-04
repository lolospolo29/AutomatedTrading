from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray


class InversionFVG:
    @staticmethod
    def return_pd_array(last_candle:Candle, fvg:PDArray)->bool:

        candles = sorted(fvg.candles,key = lambda x :x.iso_time)
        first_candle:Candle = candles[0]

        if fvg.direction == "Bullish":
            if last_candle.close < first_candle.high:
                return True
        if fvg.direction == "Bearish":
            if last_candle.close > first_candle.low:
                return True
        return False