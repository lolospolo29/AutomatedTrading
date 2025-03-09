from files.models.asset.Candle import Candle
from files.models.frameworks.PDArray import PDArray


class NDOG:
    @staticmethod
    def detect_ndog(first_candle:Candle, second_candle:Candle)->PDArray:
        if first_candle.iso_time.day != second_candle.iso_time.day:
            return PDArray(candles=[first_candle, second_candle],name="NDOG")