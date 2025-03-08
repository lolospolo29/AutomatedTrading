from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray


class NWOG:
    @staticmethod
    def detect_nwog(first_candle:Candle, second_candle:Candle)-> PDArray:
        if first_candle.iso_time.hour == 16 and first_candle.iso_time.minute == 59 and second_candle.iso_time.hour == 0:
            return PDArray(candles=[first_candle, second_candle],name="NDOG")