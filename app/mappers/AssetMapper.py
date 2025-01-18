import threading

from app.models.asset.Candle import Candle


class AssetMapper:

    @staticmethod
    def map_candle_from_trading_view(json: dict) -> Candle:
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
