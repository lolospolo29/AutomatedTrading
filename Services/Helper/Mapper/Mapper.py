from typing import Any

from Models.Asset.Candle import Candle
from Models.Trade.Order import Order
from Models.Trade.Trade import Trade


class Mapper:
    def MapToClass(self, data: Any) -> Any:

        if "_id" in data and len(data) > 1:
            # Case 1: Filter out MongoDB-specific fields like "_id"
            mainData = {k: v for k, v in data.items() if k != "_id"}
        else:
            # Case 2: Assume data does not follow the MongoDB structure directly
            mainData = data

        if not mainData:
            raise ValueError("No valid data fields found in the input data.")

        # Now proceed with the mapping as per the main data key
        name = list(mainData.keys())[0]

        # name = list(data.keys())[0]

        if name == "Candle":
            return self.mapCandle(mainData)

        if name == "Trade":
            return self.mapTrade(mainData)

        if name == "order":
            return self.mapOrder(mainData)

        return None

    def mapTrade(self, maindata: Any) -> Trade:
        # Mappe die Daten auf das Trade-Objekt
        maindata = maindata.get("Trade")

        # Handle asset
        assetValue = maindata.get('asset')
        assetValue = assetValue.strip("'") if assetValue else None  # Entferne einfache Anführungszeichen

        # Handle strategyName
        strategyName = maindata.get('strategyName', '')

        # Initialisiere das Trade-Objekt
        trade = Trade(asset=assetValue, strategy=strategyName)

        # Mappe den Status und PnL
        trade.status = maindata.get('status', None)
        trade.pnl = maindata.get('pnl', 0)

        # Verarbeite die Order-Liste, falls vorhanden
        orderJSON = maindata.get('orders')
        for orderData in orderJSON:
            trade.orders.append(self.MapToClass(orderData))

        return trade

    @staticmethod
    def mapOrder(data: Any) -> Order:
        order = Order()
        order.status = data.get('status')
        order.id = data.get('id')
        order.stopLoss = data.get('stopLoss')
        order.takeProfit = data.get('takeProfit')
        order.riskPercentage = data.get('riskPercentage')
        order.broker = data.get('broker')
        return order

    @staticmethod
    def mapCandle(mainData: Any) -> Candle:
            mainData = mainData.get("Candle")
            asset = mainData.get("asset")
            broker = mainData.get("broker")
            open = mainData.get("open")
            close = mainData.get("close")
            high = mainData.get("high")
            low = mainData.get("low")
            IsoTime = mainData.get("IsoTime")
            timeFrame = mainData.get("timeFrame")

            return Candle(asset,broker,open,close,high,low,IsoTime,timeFrame)
