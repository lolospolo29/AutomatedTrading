from typing import Any

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

        if name == "Trade":
            return self.mapTrade(data)

        if name == "order":
            return self.mapOrder(data)

        return None

    def mapTrade(self, data: Any) -> Trade:
        # Mappe die Daten auf das Trade-Objekt
        data = data.get("Trade")

        # Handle asset
        assetValue = data.get('asset')
        assetValue = assetValue.strip("'") if assetValue else None  # Entferne einfache Anführungszeichen

        # Handle strategyName
        strategyName = data.get('strategyName', '')

        # Initialisiere das Trade-Objekt
        trade = Trade(asset=assetValue, strategyName=strategyName)

        # Mappe den Status und PnL
        trade.status = data.get('status', None)
        trade.pnl = data.get('pnl', 0)

        # Verarbeite die Order-Liste, falls vorhanden
        orderJSON = data.get('orders')
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
