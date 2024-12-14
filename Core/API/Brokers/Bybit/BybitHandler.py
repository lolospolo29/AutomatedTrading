# region Imports
import json
import threading
import time

from Core.API.Brokers.Bybit.Bybit import Bybit
from Core.API.Brokers.Bybit.GET.OpenAndClosedOrders import OpenAndClosedOrders
from Core.API.Brokers.Bybit.GET.PostionInfo import PositionInfo
from Core.API.Brokers.Bybit.GET.Response.OpenAndClosedOrdersAll import OpenAndClosedOrdersAll
from Core.API.Brokers.Bybit.GET.Response.PositionInfoAll import PositionInfoAll
from Core.API.Brokers.Bybit.GET.Response.TickersLinearInverse import TickersLinearInverse
from Core.API.Brokers.Bybit.GET.Response.TickersOption import TickersOption
from Core.API.Brokers.Bybit.GET.Response.TickersSpot import TickersSpot
from Core.API.Brokers.Bybit.GET.Tickers import Tickers
from Core.API.Brokers.Bybit.POST.AddOrReduceMargin import AddOrReduceMargin
from Core.API.Brokers.Bybit.POST.AmendOrder import AmendOrder
from Core.API.Brokers.Bybit.POST.CancelAllOrers import CancelAllOrders
from Core.API.Brokers.Bybit.POST.CancelOrder import CancelOrder
from Core.API.Brokers.Bybit.POST.PlaceOrder import PlaceOrder
from Core.API.Brokers.Bybit.POST.Response.AddOrReduceMarginAll import AddOrReduceMarginAll
from Core.API.Brokers.Bybit.POST.Response.AmendOrderAll import AmendOrderAll
from Core.API.Brokers.Bybit.POST.Response.BatchAmendOrder import BatchAmendOrder
from Core.API.Brokers.Bybit.POST.Response.BatchCancelOrder import BatchCancelOrder
from Core.API.Brokers.Bybit.POST.Response.BatchPlaceOrder import BatchPlaceOrder
from Core.API.Brokers.Bybit.POST.Response.CancelAllOrdersAll import CancelAllOrdersAll
from Core.API.Brokers.Bybit.POST.Response.CancelOrderAll import CancelOrderAll
from Core.API.Brokers.Bybit.POST.Response.PlaceOrderAll import PlaceOrderAll
from Core.API.Brokers.Bybit.POST.SetLeverage import SetLeverage
from Core.API.Brokers.Bybit.POST.TradingStop import TradingStop
from Core.API.ResponseParams import ResponseParams
# endregion

class BybitHandler:
    def __init__(self):
        self.name = "Bybit"
        self.broker: Bybit = Bybit("Bybit")
        self.isLockActive = False

        self.amendBatch: dict[str, list[AmendOrder]] = {}
        self.amendLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

        self.cancelOrderBatch: dict[str, list[CancelOrder]] = {}
        self.cancelLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

        self.placeOrderBatch: dict[str, list[PlaceOrder]] = {}
        self.placeLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

    # region GET Methods

    def returnOpenAndClosedOrder(self,**kwargs) -> OpenAndClosedOrdersAll:

        openAndClosedOrders: OpenAndClosedOrders = OpenAndClosedOrders(**kwargs)

        # Validierung der Eingabeparameter
        if not openAndClosedOrders.validate():
            raise ValueError("The Fields that were required were not given")

        params = openAndClosedOrders.toQueryString()

        endPoint = "/v5/order/realtime"
        method = "GET"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], OpenAndClosedOrdersAll)

        return result

    def returnPositionInfo(self, **kwargs) -> PositionInfo:

        positionInfo: PositionInfo = PositionInfo(**kwargs)

        # Validierung der Eingabeparameter
        if not positionInfo.validate():
            raise ValueError("The Fields that were required were not given")

        params = positionInfo.toQueryString()

        endPoint = "/v5/position/list"
        method = "GET"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], PositionInfoAll)

        return result

    def returnTickers(self, **kwargs):

        tickers: Tickers = Tickers(**kwargs)

        # Validierung der Eingabeparameter
        if not tickers.validate():
            raise ValueError("The Fields that were required were not given")

        params = tickers.toQueryString()

        endPoint = "/v5/market/tickers"
        method = "GET"

        responseJson = self.broker.sendRequest(endPoint, method, params)

        responseParams = ResponseParams()

        if tickers.category == "linear" or tickers.category == "inverse":
            result = responseParams.fromDict(responseJson['result'], TickersLinearInverse)
            return result

        elif tickers.category == "option":
            result = responseParams.fromDict(responseJson['result'], TickersOption)
            return result

        elif tickers.category == "spot":
            result = responseParams.fromDict(responseJson['result'], TickersSpot)
            return result

    def returnTickersLinearInverse(self,**kwargs) -> TickersLinearInverse:
        return self.returnTickers(**kwargs)

    def returnTickersOption(self,**kwargs) -> TickersOption:
        return self.returnTickers(**kwargs)

    def returnTickersSpot(self,**kwargs) -> TickersSpot:
        return self.returnTickers(**kwargs)

    # endregion

    # region POST Methods
    def addOrReduceMargin(self, **kwargs) -> AddOrReduceMarginAll:

        addOrReduceMargin: AddOrReduceMargin = AddOrReduceMargin(**kwargs)

        # Validierung der Eingabeparameter
        if not addOrReduceMargin.validate():
            raise ValueError("The Fields that were required were not given")

        params = addOrReduceMargin.toDict()

        endPoint = "/v5/position/add-margin"
        method = "POST"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], AddOrReduceMarginAll)

        return result

    def amendOrder(self, **kwargs) -> AmendOrderAll:
        amendOrder: AmendOrder = AmendOrder(**kwargs)

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = amendOrder.toDict()

        endPoint = "/v5/order/amend"
        method = "POST"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], AmendOrderAll)

        return result

    def cancelAllOrders(self,**kwargs) -> CancelAllOrdersAll:
        cancelOrders: CancelAllOrders = CancelAllOrders(**kwargs)

        # Validierung der Eingabeparameter
        if not cancelOrders.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrders.toDict()

        endPoint = "/v5/order/cancel-all"
        method = "POST"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], CancelAllOrdersAll)

        return result

    def cancelOrder(self, **kwargs) -> CancelOrderAll:
        cancelOrder: CancelOrder = CancelOrder(**kwargs)

        # Validierung der Eingabeparameter
        if not cancelOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrder.toDict()

        endPoint = "/v5/order/cancel"
        method = "POST"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], CancelOrderAll)

        return result

    def placeOrder(self, **kwargs) -> PlaceOrderAll:
        placeOrder: PlaceOrder = PlaceOrder(**kwargs)

        # Validierung der Eingabeparameter
        if not placeOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = placeOrder.toDict()

        endPoint = "/v5/order/create"
        method = "POST"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], PlaceOrderAll)

        return result

    def setLeverage(self, **kwargs) -> bool:
        setLeverage: SetLeverage = SetLeverage(**kwargs)

        # Validierung der Eingabeparameter
        if not setLeverage.validate():
            raise ValueError("The Fields that were required were not given")

        params = setLeverage.toDict()

        endPoint = "/v5/position/set-leverage"
        method = "POST"

        responseJson = self.broker.sendRequest(endPoint, method, params)

        if responseJson.get("retMsg") == "OK":
            return True
        return False

    def setTradingStop(self, **kwargs) -> bool:
        tradingStop: TradingStop = TradingStop(**kwargs)

        # Validierung der Eingabeparameter
        if not tradingStop.validate():
            raise ValueError("The Fields that were required were not given")

        params = tradingStop.toDict()

        endPoint = "/v5/position/trading-stop"
        method = "POST"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        if responseJson.get("retMsg") == "OK":
            return True
        return False

    # endregion

    # region Batch Methods
    def batchAmendOrder(self, category, **kwargs) -> BatchAmendOrder:
        amendOrder: AmendOrder = AmendOrder(**kwargs)

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        # Initialisiere die Kategorie, falls sie nicht existiert
        if category not in self.amendBatch:
            self.amendBatch[category] = []
            self.amendLockStatus[category] = False

        # Warte, falls die Kategorie gesperrt ist
        while self.amendLockStatus[category]:
            time.sleep(1)

        # Füge die Order zur Kategorie-Liste hinzu
        self.amendBatch[category].append(amendOrder)

        # Verarbeite die Batch-Order, wenn dies die erste Order der Kategorie ist
        if len(self.amendBatch[category]) == 1:
            endPoint = "/v5/order/amend-batch"
            method = "POST"

            time.sleep(60)

            # Sperre die Kategorie
            self.amendLockStatus[category] = True

            # Erstelle Payload für die aktuelle Kategorie
            payload = {
                "category": category,
                "request": [
                    {k: v for k, v in vars(order).items() if v is not None and k not in ["category"]}
                    for order in self.amendBatch[category]
                ]
            }

            responseJson = self.broker.sendRequest(endPoint, method, payload)

            # Nach dem Senden der Anfrage: Liste leeren und Lock aufheben
            self.amendBatch[category] = []
            self.amendLockStatus[category] = False

            # Verarbeite die Antwort
            responseParams = ResponseParams()
            result = responseParams.fromDict(responseJson['result'], BatchAmendOrder)

            return result

    def batchCancelOrder(self, category, **kwargs) -> BatchCancelOrder:
        cancelOrder: CancelOrder = CancelOrder(**kwargs)

        # Validierung der Eingabeparameter
        if not cancelOrder.validate():
            raise ValueError("The Fields that were required were not given")

        # Initialisiere die Kategorie, falls sie nicht existiert
        if category not in self.cancelOrderBatch:
            self.cancelOrderBatch[category] = []
            self.cancelLockStatus[category] = False

        # Warte, falls die Kategorie gesperrt ist
        while self.cancelLockStatus[category]:
            time.sleep(1)

        # Füge die Order zur Kategorie-Liste hinzu
        self.cancelOrderBatch[category].append(cancelOrder)

        # Verarbeite die Batch-Order, wenn dies die erste Order der Kategorie ist
        if len(self.cancelOrderBatch[category]) == 1:
            endPoint = "/v5/order/cancel-batch"
            method = "POST"

            time.sleep(60)

            # Sperre die Kategorie
            self.cancelLockStatus[category] = True

            # Erstelle Payload für die aktuelle Kategorie
            payload = {
                "category": category,
                "request": [
                    {k: v for k, v in vars(order).items() if v is not None and k not in ["category"]}
                    for order in self.cancelOrderBatch[category]
                ]
            }

            responseJson = self.broker.sendRequest(endPoint, method, payload)

            # Nach dem Senden der Anfrage: Liste leeren und Lock aufheben
            self.cancelOrderBatch[category] = []
            self.cancelLockStatus[category] = False

            # Verarbeite die Antwort
            responseParams = ResponseParams()
            result = responseParams.fromDict(responseJson['result'], BatchCancelOrder)

            return result

    def batchPlaceOrder(self, category, **kwargs) -> BatchPlaceOrder:
        placeOrder: PlaceOrder = PlaceOrder(**kwargs)

        # Validierung der Eingabeparameter
        if not placeOrder.validate(batchOrder=True):
            raise ValueError("The Fields that were required were not given")

        # Initialisiere die Kategorie, falls sie nicht existiert
        if category not in self.placeOrderBatch:
            self.placeOrderBatch[category] = []
            self.placeLockStatus[category] = False

        # Warte, falls die Kategorie gesperrt ist
        while self.placeLockStatus[category]:
            time.sleep(1)

        # Füge die Order zur Kategorie-Liste hinzu
        self.placeOrderBatch[category].append(placeOrder)

        # Verarbeite die Batch-Order, wenn dies die erste Order der Kategorie ist
        if len(self.placeOrderBatch[category]) == 1:
            endPoint = "/v5/order/create-batch"
            method = "POST"

            time.sleep(10)

            # Sperre die Kategorie
            self.placeLockStatus[category] = True

            # Erstelle Payload für die aktuelle Kategorie
            payload = {
                "category": category,
                "request": [
                    {k: v for k, v in vars(order).items() if v is not None and k not in ["category"]}
                    for order in self.placeOrderBatch[category]
                ]
            }

            responseJson = self.broker.sendRequest(endPoint, method,json.dumps(payload))

            # Nach dem Senden der Anfrage: Liste leeren und Lock aufheben
            self.placeOrderBatch[category] = []
            self.placeLockStatus[category] = False

            # Verarbeite die Antwort
            responseParams = ResponseParams()
            result = responseParams.fromDict(responseJson['result'], BatchAmendOrder)

            return result

    # endregion

handler = BybitHandler()

def place_single_order(category, symbol, side, orderType, qty, price,orderLinkId,timeInForce):
    handler.batchPlaceOrder(category,symbol=symbol, side=side, orderType=orderType, qty=qty, price=price,orderLinkId=orderLinkId,timeInForce=timeInForce)

# Parameter für die Orders
order1 = {"category": "linear", "symbol": "ETHUSDT", "side": "Buy", "orderType": "Market", "qty": "0.3", "price": "3000","orderLinkId":"12313131","timeInForce":"PostOnly"}
order2 = {"category": "linear", "symbol": "BTCUSDT", "side": "Buy", "orderType": "Market", "qty": "0.4", "price": "3030","orderLinkId":"331313","timeInForce":"PostOnly" }

# Starte separate Threads für jede Order
thread1 = threading.Thread(target=place_single_order, kwargs=order1)
thread2 = threading.Thread(target=place_single_order, kwargs=order2)

# Threads starten
thread1.start()
time.sleep(4)
thread2.start()

# Warten, bis die Threads abgeschlossen sind
thread1.join()
thread2.join()

print("Jede Order wurde in einem separaten Thread getestet!")
