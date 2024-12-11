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
from Core.API.Brokers.Bybit.POST.Response.BatchAmendOrder import BatchAmendOrderAll
from Core.API.Brokers.Bybit.POST.Response.CancelAllOrdersAll import CancelAllOrdersAll
from Core.API.Brokers.Bybit.POST.Response.CancelOrderAll import CancelOrderAll
from Core.API.Brokers.Bybit.POST.Response.PlaceOrderAll import PlaceOrderAll
from Core.API.Brokers.Bybit.POST.SetLeverage import SetLeverage
from Core.API.Brokers.Bybit.POST.TradingStop import TradingStop
from Core.API.ResponseParams import ResponseParams


class BybitHandler:
    def __init__(self, broker: Bybit):
        self.broker: Bybit = broker
        self.isLockActive = False
        self.amendBatch: list[AmendOrder] = []

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
    def batchAmendOrder(self,**kwargs)-> BatchAmendOrderAll:
        amendOrder: AmendOrder = AmendOrder(**kwargs)

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        self.amendBatch.append(amendOrder)

        if len(self.amendBatch) == 1:

            endPoint = "/v5/order/amend-batch"
            method = "POST"

            responseJson = self.broker.sendRequest(endPoint, method, params)
            responseParams = ResponseParams()
            result = responseParams.fromDict(responseJson['result'], BatchAmendOrderAll)

            return result

    # endregion




handler = BybitHandler(broker=Bybit("Bybit"))

# Aufruf mit nur einigen Parametern
response = handler.returnTickersLinearInverse(category="linear", symbol="BTCUSDT")
