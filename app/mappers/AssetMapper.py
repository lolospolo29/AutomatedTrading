import threading

from app.models.asset.Candle import Candle


class AssetMapper:

    @staticmethod
    def mapCandleFromTradingView(json: dict) -> Candle:
        mainData = json.get("Candle")
        asset = json.get("asset")
        broker = json.get("broker")
        open = json.get("open")
        close = mainData.get("close")
        high = mainData.get("high")
        low = mainData.get("low")
        IsoTime = mainData.get("IsoTime")
        timeFrame = mainData.get("timeFrame")

        return Candle(asset, broker, open, high, low, close, IsoTime, timeFrame)

        # if "_id" in data and len(data) > 1:
        #     # Case 1: Filter out MongoDB-specific fields like "_id"
        #     mainData = {k: v for k, v in data.items() if k != "_id"}