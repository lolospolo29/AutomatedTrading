from Models.API.Brokers.Bybit.GET.OpenAndClosedOrders import OpenAndClosedOrders
from Models.API.Brokers.Bybit.GET.PostionInfo import PositionInfo
from Models.API.Brokers.Bybit.GET.Response.OpenAndClosedOrdersAll import OpenAndClosedOrdersAll
from Models.API.Brokers.Bybit.GET.Response.PositionInfoAll import PositionInfoAll
from Models.API.Brokers.Bybit.GET.Response.TickersLinearInverse import TickersLinearInverse
from Models.API.Brokers.Bybit.GET.Response.TickersOption import TickersOption
from Models.API.Brokers.Bybit.GET.Response.TickersSpot import TickersSpot
from Models.API.Brokers.Bybit.GET.Tickers import Tickers
from Models.API.Brokers.Bybit.POST.AddOrReduceMargin import AddOrReduceMargin
from Models.API.Brokers.Bybit.POST.Response.AddOrReduceMarginAll import AddOrReduceMarginAll
from Models.API.ResponseParams import ResponseParams
from Models.Main.Brokers.Crypto.Bybit import Bybit


class BybitHandler:
    def __init__(self, broker: Bybit):
        self.broker: Bybit = broker

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
    # endregion



handler = BybitHandler(broker=Bybit("Bybit"))

# Aufruf mit nur einigen Parametern
response = handler.returnTickersLinearInverse(category="linear", symbol="BTCUSDT")
