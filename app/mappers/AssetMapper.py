from app.models.asset.Candle import Candle
from app.monitoring.logging.logging_startup import logger


class AssetMapper:
    """Maps the Candles from TradingView"""

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
            logger.debug(json)
            candle = json.get("Candle")
            asset = candle.get("asset")
            broker = candle.get("broker")
            open = candle.get("open")
            close = candle.get("close")
            high = candle.get("high")
            low = candle.get("low")
            iso_time = candle.get("iso_time")
            timeFrame = candle.get("timeframe")
            return Candle(asset, broker, open, high, low, close, iso_time, timeFrame)
        except Exception as e:
            ValueError("Mapping Tradingview Candle Error: {}".format(e))
