from app.models.asset.Candle import Candle

class NDOG:
    @staticmethod
    def is_ndog(first_candle:Candle, second_candle:Candle)->bool:
        if first_candle.iso_time.hour == 23 and second_candle.iso_time.minute == 59 and second_candle.iso_time.hour == 0 and second_candle.iso_time.minute == 0:
            return True
        return False