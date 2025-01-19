from app.mappers.exceptions.MappingFailedExceptionError import MappingFailedExceptionError
from app.models.asset.Candle import Candle


class AssetMapper:
    @staticmethod
    def map_candle_from_trading_view(json: dict) -> Candle:
        """
        Updates the attributes of a regular class instance with values from a dataclass instance.

        Args:
            json: json from Tradingview

        Returns:
            Candle for Asset.
        """
        try:
            candle = json.get("Candle")
            asset = candle.get("asset")
            broker = candle.get("broker")
            open = candle.get("open")
            close = candle.get("close")
            high = candle.get("high")
            low = candle.get("low")
            iso_time = candle.get("IsoTime")
            timeFrame = candle.get("timeFrame")
            return Candle(asset, broker, open, high, low, close, iso_time, timeFrame)
        except Exception as e:
            raise MappingFailedExceptionError("Candle")
