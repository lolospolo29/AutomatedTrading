import threading

from app.models.asset.Candle import Candle


class AssetMapper:

    @staticmethod
    def mapCandleFromTradingView(json: dict) -> Candle:
        candle = json.get("Candle")
        asset = candle.get("asset")
        broker = candle.get("broker")
        open = candle.get("open")
        close = candle.get("close")
        high = candle.get("high")
        low = candle.get("low")
        IsoTime = candle.get("IsoTime")
        timeFrame = candle.get("timeFrame")

        return Candle(asset, broker, open, high, low, close, IsoTime, timeFrame)

        # if "_id" in data and len(data) > 1:
        #     # Case 1: Filter out MongoDB-specific fields like "_id"
        #     mainData = {k: v for k, v in data.items() if k != "_id"}