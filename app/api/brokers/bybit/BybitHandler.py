# region Imports
import json
import time
from typing import Any

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.Bybit import Bybit
from app.api.brokers.bybit.BybitMapper import BybitMapper
from app.api.brokers.bybit.enums.EndPointEnum import EndPointEnum

from app.api.brokers.bybit.enums.OpenOnlyEnum import OpenOnlyEnum
from app.api.brokers.bybit.get.OpenAndClosedOrders import OpenAndClosedOrders
from app.api.brokers.bybit.get.PostionInfo import PositionInfo
from app.api.brokers.bybit.reponse.get.OpenAndClosedOrdersAll import OpenAndClosedOrdersAll
from app.api.brokers.bybit.reponse.get.PositionInfoAll import PositionInfoAll
from app.api.brokers.bybit.reponse.get.TickersLinearInverse import TickersLinearInverse
from app.api.brokers.bybit.reponse.get.TickersOption import TickersOption
from app.api.brokers.bybit.reponse.get.TickersSpot import TickersSpot
from app.api.brokers.bybit.get.Tickers import Tickers
from app.api.brokers.bybit.post.AddOrReduceMargin import AddOrReduceMargin
from app.api.brokers.bybit.post.AmendOrder import AmendOrder
from app.api.brokers.bybit.post.CancelAllOrers import CancelAllOrders
from app.api.brokers.bybit.post.CancelOrder import CancelOrder
from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.api.brokers.bybit.reponse.post.AddOrReduceMarginAll import AddOrReduceMarginAll
from app.api.brokers.bybit.reponse.post.AmendOrderAll import AmendOrderAll
from app.api.brokers.bybit.reponse.post.BatchAmendOrder import BatchAmendOrder
from app.api.brokers.bybit.reponse.post.BatchCancelOrder import BatchCancelOrder
from app.api.brokers.bybit.reponse.post.BatchPlaceOrder import BatchPlaceOrder
from app.api.brokers.bybit.reponse.post.CancelAllOrdersAll import CancelAllOrdersAll
from app.api.brokers.bybit.reponse.post.CancelOrderAll import CancelOrderAll
from app.api.brokers.bybit.reponse.post.PlaceOrderAll import PlaceOrderAll
from app.api.brokers.bybit.post.SetLeverage import SetLeverage
from app.api.brokers.bybit.post.TradingStop import TradingStop
from app.models.trade.Order import Order


# endregion

class BybitHandler:
    def __init__(self):
        self.name = "bybit"
        self.broker: Bybit = Bybit("bybit")
        self._bybitMapper = BybitMapper()
        self.isLockActive = False

        self.amendBatch: dict[str, list[AmendOrder]] = {}
        self.amendLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

        self.cancelOrderBatch: dict[str, list[CancelOrder]] = {}
        self.cancelLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

        self.placeOrderBatch: dict[str, list[PlaceOrder]] = {}
        self.placeLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

    # region get Methods

    def returnOpenAndClosedOrder(self,order: Order,baseCoin:str=None,settleCoin:str=None,openOnly:OpenOnlyEnum=None
                                 ,limit:int=20,cursor:str=None) -> OpenAndClosedOrdersAll:

        openAndClosedOrders: OpenAndClosedOrders = (self._bybitMapper.mapOrderToOpenAndClosedOrders
                                                    (order,baseCoin,settleCoin,openOnly,limit,cursor))

        # Validierung der Eingabeparameter
        if not openAndClosedOrders.validate():
            raise ValueError("The Fields that were required were not given")

        params = openAndClosedOrders.toQueryString()

        endPoint = EndPointEnum.OPENANDCLOSED.value
        method = "get"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], OpenAndClosedOrdersAll)

        return result

    def returnPositionInfo(self,order: Order,baseCoin:str=None,settleCoin:str=None
                                 ,limit:int=20,cursor:str=None) -> PositionInfoAll:

        positionInfo: PositionInfo = self._bybitMapper.mapOrderToPositionInfo(order,baseCoin,settleCoin,limit,cursor)

        # Validierung der Eingabeparameter
        if not positionInfo.validate():
            raise ValueError("The Fields that were required were not given")

        params = positionInfo.toQueryString()

        endPoint = EndPointEnum.POSITIONINFO.value
        method = "get"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], PositionInfoAll)

        return result

    def returnTickers(self, **kwargs) -> Any:

        tickers: Tickers = Tickers(**kwargs)

        # Validierung der Eingabeparameter
        if not tickers.validate():
            raise ValueError("The Fields that were required were not given")

        params = tickers.toQueryString()

        endPoint = "/v5/market/tickers"
        method = "get"

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

    # region post Methods
    def addOrReduceMargin(self, **kwargs) -> AddOrReduceMarginAll:

        addOrReduceMargin: AddOrReduceMargin = AddOrReduceMargin(**kwargs)

        # Validierung der Eingabeparameter
        if not addOrReduceMargin.validate():
            raise ValueError("The Fields that were required were not given")

        params = addOrReduceMargin.toDict()

        endPoint = "/v5/position/add-margin"
        method = "post"

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
        method = "post"

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
        method = "post"

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
        method = "post"

        responseJson = self.broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], CancelOrderAll)

        return result

    def placeOrder(self, order: Order) -> PlaceOrderAll:

        placeOrder: PlaceOrder = self._bybitMapper.mapOrderToPlaceOrder(order)

        # Validierung der Eingabeparameter
        if not placeOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = placeOrder.toDict()

        endPoint = "/v5/order/create"
        method = "post"

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
        method = "post"

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
        method = "post"

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
            method = "post"

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
            method = "post"

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
            method = "post"

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

    # Logic for Handling Failed Requests and Logging
