# region Imports
import time

from app.api.brokers.bybit.Bybit import Bybit
from app.api.brokers.bybit.enums.EndPointEnum import EndPointEnum
from app.api.brokers.bybit.enums.RateLimitEnum import RateLimitEnum
from app.api.brokers.bybit.get.OpenAndClosedOrders import OpenAndClosedOrders
from app.api.brokers.bybit.get.OrderHistory import OrderHistory
from app.api.brokers.bybit.get.PostionInfo import PositionInfo
from app.api.brokers.bybit.post.AmendOrder import AmendOrder
from app.api.brokers.bybit.post.CancelAllOrers import CancelAllOrders
from app.api.brokers.bybit.post.CancelOrder import CancelOrder
from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.api.brokers.bybit.post.SetLeverage import SetLeverage
from app.api.brokers.models.BrokerOrder import BrokerOrder
from app.api.brokers.models.BrokerPosition import BrokerPosition
from app.helper.registry.RateLimitRegistry import RateLimitRegistry
from app.interfaces.IBrokerHandler import IBrokerHandler
from app.mappers.ClassMapper import ClassMapper
from app.api.brokers.models.RequestParameters import RequestParameters
from app.monitoring.retryRequest import retry_request

# endregion

rate_limit_registry = RateLimitRegistry(RateLimitEnum)

class BybitHandler(IBrokerHandler):

    def __init__(self):
        self.name = "BYBIT"
        self.__broker: Bybit = Bybit("BYBIT")
        self.isLockActive = False
        self._bybitMapper = ClassMapper()
        self._rateLimitRegistry = RateLimitRegistry(RateLimitEnum)


    # region get Methods
    @rate_limit_registry.rate_limited
    def returnOpenAndClosedOrder(self,requestParams: RequestParameters) -> list[BrokerOrder]:

        openAndClosedOrders: OpenAndClosedOrders = (self._bybitMapper.map_args_to_dataclass
                                                    (OpenAndClosedOrders,requestParams,RequestParameters))


        # Validierung der Eingabeparameter
        if not openAndClosedOrders.validate():
            raise ValueError("The Fields that were required were not given")


        endPoint = EndPointEnum.OPENANDCLOSED.value
        method = "get"

        brokerOrderList: list[BrokerOrder] = []
        previousCursor:str = ""

        while True:

            params = openAndClosedOrders.toQueryString()
            responseJson = self.__broker.sendRequest(endPoint, method, params)

            objList = responseJson.get("result").get("list")
            nextPageCursor:str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
               brokerOrderList.append(self._bybitMapper.map_dict_to_dataclass(obj, BrokerOrder))

            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            openAndClosedOrders.cursor = nextPageCursor

        return brokerOrderList

    @rate_limit_registry.rate_limited
    def returnPositionInfo(self,requestParams:RequestParameters) -> list[BrokerPosition]:

        positionInfo: PositionInfo = (self._bybitMapper.map_args_to_dataclass
                                      (PositionInfo,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not positionInfo.validate():
            raise ValueError("The Fields that were required were not given")


        endPoint = EndPointEnum.POSITIONINFO.value
        method = "get"

        brokerPositionList: list[BrokerPosition] = []
        previousCursor:str = ""

        while True:

            params = positionInfo.toQueryString()
            responseJson = self.__broker.sendRequest(endPoint, method, params)

            objList = responseJson.get("result").get("list")
            nextPageCursor:str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
               brokerPositionList.append(self._bybitMapper.map_dict_to_dataclass(obj, BrokerPosition))

            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            positionInfo.cursor = nextPageCursor


        return brokerPositionList

    @rate_limit_registry.rate_limited
    def returnOrderHistory(self,requestParams: RequestParameters) -> list[BrokerOrder]:

        orderHistory: OrderHistory = (self._bybitMapper.map_args_to_dataclass
                                                    (OrderHistory,requestParams,RequestParameters))


        # Validierung der Eingabeparameter
        if not orderHistory.validate():
            raise ValueError("The Fields that were required were not given")

        endPoint = EndPointEnum.HISTORY.value
        method = "get"

        brokerOrderList: list[BrokerOrder] = []
        previousCursor:str = ""

        while True:

            params = orderHistory.toQueryString()
            responseJson = self.__broker.sendRequest(endPoint, method, params)

            objList = responseJson.get("result").get("list")
            nextPageCursor:str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
                brokerOrderList.append(self._bybitMapper.map_dict_to_dataclass(obj, BrokerOrder))

            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            orderHistory.cursor = nextPageCursor

        return brokerOrderList

    # endregion

    # region post Methods
    @rate_limit_registry.rate_limited
    def amendOrder(self,requestParams:RequestParameters) -> BrokerOrder:
        amendOrder: AmendOrder = (self._bybitMapper.map_args_to_dataclass
                                  (AmendOrder,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = amendOrder.toDict()

        endPoint = EndPointEnum.AMEND.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], BrokerOrder)

        return result

    @rate_limit_registry.rate_limited
    def cancelAllOrders(self,requestParams:RequestParameters) -> list[BrokerOrder]:

        cancelOrders: CancelAllOrders = (self._bybitMapper.map_args_to_dataclass
                                         (CancelAllOrders,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not cancelOrders.validate():
            raise ValueError("The Fields that were required were not given")

        endPoint = EndPointEnum.CANCELALL.value
        method = "post"

        params = cancelOrders.toDict()

        brokerOrderList: list[BrokerOrder] = []

        responseJson = self.__broker.sendRequest(endPoint, method, params)

        objList = responseJson.get("result").get("list")

        for obj in objList:
            brokerOrderList.append(self._bybitMapper.map_dict_to_dataclass(obj, BrokerOrder))

        return brokerOrderList

    @rate_limit_registry.rate_limited
    def cancelOrder(self,requestParams:RequestParameters) -> BrokerOrder:
        cancelOrder: CancelOrder = (self._bybitMapper.map_args_to_dataclass
                                    (CancelOrder,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not cancelOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrder.toDict()

        endPoint = EndPointEnum.CANCEL.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], BrokerOrder)

        return result

    @rate_limit_registry.rate_limited
    def placeOrder(self,requestParams:RequestParameters) -> BrokerOrder:

        placeOrder: PlaceOrder = (self._bybitMapper.map_args_to_dataclass
                                  (PlaceOrder,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not placeOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = placeOrder.toDict()

        endPoint = EndPointEnum.PLACEORDER.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], BrokerOrder)

        return result

    @rate_limit_registry.rate_limited
    def setLeverage(self,requestParams:RequestParameters) -> bool:
        time.sleep(5)
        setLeverage: SetLeverage = (self._bybitMapper.map_args_to_dataclass
                                    (SetLeverage,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not setLeverage.validate():
            raise ValueError("The Fields that were required were not given")

        params = setLeverage.toDict()

        endPoint = EndPointEnum.SETLEVERAGE.value
        method = "post"

        def request_function():
            """Encapsulated API request logic for retry utility."""
            responseJson = self.__broker.sendRequest(endPoint, method, params)
            if not responseJson.get("retMsg") == "OK":
                raise ValueError(responseJson.get("retMsg"))
        # Use retry utility to handle retries
        return retry_request(request_function)

    # endregion

# bh = BybitHandler()
# request = RequestParameters()
# request.category = "linear"
# request.symbol = "XRPUSDT"
# request.orderLinkId = "6"
# request.side = "Buy"
# request.qty = str(6)
# request.orderType = "Limit"
# request.triggerPrice = "1.9"
# request.price = "1.9"
# bh.cancelAllOrders(request)

