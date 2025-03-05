from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.frameworks.Structure import Structure


class MSS:
    @staticmethod
    def detect_mss(last_candle:Candle,swing:PDArray):
        if swing.status != "Sweeped":
            if swing.direction == "Bullish":
                highest_candle:Candle = sorted(swing.candles, key=lambda candle: candle.high,reverse= True)[-1]
                if highest_candle.high < last_candle.close:
                    return Structure(name="MSS",candles=[highest_candle],reference=swing.id,direction="Bullish",timeframe=last_candle.timeframe)
            if swing.direction == "Bearish":
                lowest_candle:Candle = sorted(swing.candles, key=lambda candle: candle.low)[-1]
                if lowest_candle.low > last_candle.close:
                    return Structure(name="MSS",candles=[lowest_candle],reference=swing.id,direction="Bullish",timeframe=last_candle.timeframe)