from dateutil import parser

from files.functions.to_utc import to_utc
from files.models.asset.Candle import Candle


class AssetMapper:
    @staticmethod
    def map_tradingview_json_to_candle(json: dict) -> Candle:
        candle = json.get("Candle")
        asset = candle.get("asset")
        broker = candle.get("broker")
        open = candle.get("open")
        high = candle.get("high")
        low = candle.get("low")
        close = candle.get("close")
        iso_time = candle.get("iso_time")
        dt = parser.parse(iso_time)  # Automatically detects UTC
        iso_time = to_utc(dt)
        timeframe = candle.get("timeframe")

        return Candle(asset=asset, broker=broker, open=open, high=high, low=low, close=close, timeframe=timeframe,
                   iso_time=iso_time)