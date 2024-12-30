# region Imports
import json
import time
from typing import Any
from unicodedata import category

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.Bybit import Bybit
from app.api.brokers.bybit.BybitMapper import BybitMapper
from app.api.brokers.bybit.enums.EndPointEnum import EndPointEnum

from app.api.brokers.bybit.enums.OpenOnlyEnum import OpenOnlyEnum
from app.api.brokers.bybit.enums.OrderFilterEnum import OrderFilterEnum
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
from app.models.trade.CategoryEnum import CategoryEnum
from app.models.trade.Order import Order


# endregion

class BybitHandler:

    def __init__(self):
        self.name = "bybit"
        self.__broker: Bybit = Bybit("bybit")
        self._bybitMapper = BybitMapper()
        self.isLockActive = False

        self.__amendBatch: dict[str, list[AmendOrder]] = {}
        self.__amendLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

        self.__cancelOrderBatch: dict[str, list[CancelOrder]] = {}
        self.__cancelLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

        self.__placeOrderBatch: dict[str, list[PlaceOrder]] = {}
        self.__placeLockStatus: dict[str, bool] = {}  # Kategorie -> Lock-Status

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

        responseJson = self.__broker.sendRequest(endPoint, method, params)
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

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], PositionInfoAll)

        return result

    def returnTickers(self,category:CategoryEnum,symbol:str=None,baseCoin:str=None,expDate:str=None)\
            -> Any:

        tickers: Tickers = self._bybitMapper.mapOrderToTickers(category,symbol,baseCoin,expDate)

        # Validierung der Eingabeparameter
        if not tickers.validate():
            raise ValueError("The Fields that were required were not given")

        params = tickers.toQueryString()

        endPoint = EndPointEnum.TICKERS.value
        method = "get"

        responseJson = self.__broker.sendRequest(endPoint, method, params)

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

    def returnTickersLinearInverse(self,category:CategoryEnum,symbol:str=None,baseCoin:str=None,expDate:str=None)\
            -> TickersLinearInverse:
        return self.returnTickers(category,symbol,baseCoin,expDate)

    def returnTickersOption(self,category:CategoryEnum,symbol:str=None,baseCoin:str=None,expDate:str=None) -> TickersOption:
        return self.returnTickers(category,symbol,baseCoin,expDate)

    def returnTickersSpot(self,category:CategoryEnum,symbol:str=None,baseCoin:str=None,expDate:str=None) -> TickersSpot:
        return self.returnTickers(category,symbol,baseCoin,expDate)

    # endregion

    # region post Methods
    def addOrReduceMargin(self,order:Order,margin:str=None) -> AddOrReduceMarginAll:

        addOrReduceMargin: AddOrReduceMargin = self._bybitMapper.mapOrderToModifyMargin(order,margin)

        # Validierung der Eingabeparameter
        if not addOrReduceMargin.validate():
            raise ValueError("The Fields that were required were not given")

        params = addOrReduceMargin.toDict()

        endPoint = EndPointEnum.MARGIN.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], AddOrReduceMarginAll)

        return result

    def amendOrder(self,order:Order) -> AmendOrderAll:
        amendOrder: AmendOrder = self._bybitMapper.mapOrderToAmendOrder(order)

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = amendOrder.toDict()

        endPoint = EndPointEnum.AMEND.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], AmendOrderAll)

        return result

    def cancelAllOrders(self,category:CategoryEnum=None,symbol:str=None,baseCoin:str=None,settleCoin:str=None,
                        orderFilter:OrderFilterEnum=None,stopOrderType:bool=False) -> CancelAllOrdersAll:

        cancelOrders: CancelAllOrders = self._bybitMapper.mapInputToCancelAllOrders(category,symbol,baseCoin,settleCoin,
                                                                                    orderFilter,stopOrderType)

        # Validierung der Eingabeparameter
        if not cancelOrders.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrders.toDict()

        endPoint = EndPointEnum.CANCELALL.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], CancelAllOrdersAll)

        return result

    def cancelOrder(self,order:Order) -> CancelOrderAll:
        cancelOrder: CancelOrder = self._bybitMapper.mapOrderToCancelOrder(order)

        # Validierung der Eingabeparameter
        if not cancelOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrder.toDict()

        endPoint = EndPointEnum.CANCEL.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], CancelOrderAll)

        return result

    def placeOrder(self, order: Order) -> PlaceOrderAll:

        placeOrder: PlaceOrder = self._bybitMapper.mapOrderToPlaceOrder(order)

        # Validierung der Eingabeparameter
        if not placeOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = placeOrder.toDict()

        endPoint = EndPointEnum.PLACEORDER.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        responseParams = ResponseParams()
        result = responseParams.fromDict(responseJson['result'], PlaceOrderAll)

        return result

    def setLeverage(self,category:CategoryEnum=None,symbol:str=None,buyLeverage:str=None,sellLeverage:str=None) -> bool:
        setLeverage: SetLeverage = self._bybitMapper.mapInputToSetLeverage(category,symbol,buyLeverage,sellLeverage)

        # Validierung der Eingabeparameter
        if not setLeverage.validate():
            raise ValueError("The Fields that were required were not given")

        params = setLeverage.toDict()

        endPoint = EndPointEnum.SETLEVERAGE.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)

        if responseJson.get("retMsg") == "OK":
            return True
        return False

    def setTradingStop(self,order:Order,activePrice:str=None,trailinStop:str=None) -> bool:
        tradingStop: TradingStop = self._bybitMapper.mapOrderToSetTradingStop(order,activePrice,trailinStop)

        # Validierung der Eingabeparameter
        if not tradingStop.validate():
            raise ValueError("The Fields that were required were not given")

        params = tradingStop.toDict()

        endPoint = EndPointEnum.SETTRADINGSTOP.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        if responseJson.get("retMsg") == "OK":
            return True
        return False

    # endregion

    # region Batch Methods
    def batchAmendOrder(self,order:Order) -> BatchAmendOrder:
        amendOrder: AmendOrder = self._bybitMapper.mapOrderToAmendOrder(order)
        category = amendOrder.category

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        # Initialisiere die Kategorie, falls sie nicht existiert
        if category not in self.__amendBatch:
            self.__amendBatch[category] = []
            self.__amendLockStatus[category] = False

        # Warte, falls die Kategorie gesperrt ist
        while self.__amendLockStatus[category]:
            time.sleep(1)

        # Füge die Order zur Kategorie-Liste hinzu
        self.__amendBatch[category].append(amendOrder)

        # Verarbeite die Batch-Order, wenn dies die erste Order der Kategorie ist
        if len(self.__amendBatch[category]) == 1:
            endPoint = EndPointEnum.AMENDBATCH.value
            method = "post"

            time.sleep(60)

            # Sperre die Kategorie
            self.__amendLockStatus[category] = True

            # Erstelle Payload für die aktuelle Kategorie
            payload = {
                "category": category,
                "request": [
                    {k: v for k, v in vars(order).items() if v is not None and k not in ["category"]}
                    for order in self.__amendBatch[category]
                ]
            }

            responseJson = self.__broker.sendRequest(endPoint, method, payload)

            # Nach dem Senden der Anfrage: Liste leeren und Lock aufheben
            self.__amendBatch[category] = []
            self.__amendLockStatus[category] = False

            # Verarbeite die Antwort
            responseParams = ResponseParams()
            result = responseParams.fromDict(responseJson['result'], BatchAmendOrder)

            return result

    def batchCancelOrder(self,order:Order) -> BatchCancelOrder:
        cancelOrder: CancelOrder = self._bybitMapper.mapOrderToCancelOrder(order)
        category = cancelOrder.category

        # Validierung der Eingabeparameter
        if not cancelOrder.validate():
            raise ValueError("The Fields that were required were not given")

        # Initialisiere die Kategorie, falls sie nicht existiert
        if category not in self.__cancelOrderBatch:
            self.__cancelOrderBatch[category] = []
            self.__cancelLockStatus[category] = False

        # Warte, falls die Kategorie gesperrt ist
        while self.__cancelLockStatus[category]:
            time.sleep(1)

        # Füge die Order zur Kategorie-Liste hinzu
        self.__cancelOrderBatch[category].append(cancelOrder)

        # Verarbeite die Batch-Order, wenn dies die erste Order der Kategorie ist
        if len(self.__cancelOrderBatch[category]) == 1:
            endPoint = EndPointEnum.CANCELBATCH.value
            method = "post"

            time.sleep(60)

            # Sperre die Kategorie
            self.__cancelLockStatus[category] = True

            # Erstelle Payload für die aktuelle Kategorie
            payload = {
                "category": category,
                "request": [
                    {k: v for k, v in vars(order).items() if v is not None and k not in ["category"]}
                    for order in self.__cancelOrderBatch[category]
                ]
            }

            responseJson = self.__broker.sendRequest(endPoint, method, payload)

            # Nach dem Senden der Anfrage: Liste leeren und Lock aufheben
            self.__cancelOrderBatch[category] = []
            self.__cancelLockStatus[category] = False

            # Verarbeite die Antwort
            responseParams = ResponseParams()
            result = responseParams.fromDict(responseJson['result'], BatchCancelOrder)

            return result

    def batchPlaceOrder(self,order:Order) -> BatchPlaceOrder:
        placeOrder: PlaceOrder = self._bybitMapper.mapOrderToPlaceOrder(order)
        category = placeOrder.category

        # Validierung der Eingabeparameter
        if not placeOrder.validate(batchOrder=True):
            raise ValueError("The Fields that were required were not given")

        # Initialisiere die Kategorie, falls sie nicht existiert
        if category not in self.__placeOrderBatch:
            self.__placeOrderBatch[category] = []
            self.__placeLockStatus[category] = False

        # Warte, falls die Kategorie gesperrt ist
        while self.__placeLockStatus[category]:
            time.sleep(1)

        # Füge die Order zur Kategorie-Liste hinzu
        self.__placeOrderBatch[category].append(placeOrder)

        # Verarbeite die Batch-Order, wenn dies die erste Order der Kategorie ist
        if len(self.__placeOrderBatch[category]) == 1:
            endPoint = EndPointEnum.BATCHPLACE.value
            method = "post"

            time.sleep(10)

            # Sperre die Kategorie
            self.__placeLockStatus[category] = True

            # Erstelle Payload für die aktuelle Kategorie
            payload = {
                "category": category,
                "request": [
                    {k: v for k, v in vars(order).items() if v is not None and k not in ["category"]}
                    for order in self.__placeOrderBatch[category]
                ]
            }

            responseJson = self.__broker.sendRequest(endPoint, method, json.dumps(payload))

            # Nach dem Senden der Anfrage: Liste leeren und Lock aufheben
            self.__placeOrderBatch[category] = []
            self.__placeLockStatus[category] = False

            # Verarbeite die Antwort
            responseParams = ResponseParams()
            result = responseParams.fromDict(responseJson['result'], BatchAmendOrder)

            return result

    # endregion

    # Logic for Handling Failed Requests and Logging
