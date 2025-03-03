from app.models.asset.Candle import Candle

class NWOG:
    @staticmethod
    def is_nwog(first_candle:Candle, second_candle:Candle)->bool:
        if first_candle.iso_time.hour == 16 and first_candle.iso_time.minute == 59 and second_candle.iso_time.hour == 0:
            return True
        return False