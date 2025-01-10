# region Imports
from app.api.brokers.ResponseParameters import ResponseParameters
from app.api.brokers.bybit.Bybit import Bybit
from app.api.brokers.bybit.enums.EndPointEnum import EndPointEnum
from app.api.brokers.bybit.enums.RateLimitEnum import RateLimitEnum
from app.api.brokers.bybit.get.OpenAndClosedOrders import OpenAndClosedOrders
from app.api.brokers.bybit.get.OrderHistory import OrderHistory
from app.api.brokers.bybit.get.PostionInfo import PositionInfo
from app.api.brokers.bybit.models.get.OrderHistoryAll import OrderHistoryAll
from app.api.brokers.bybit.post.AmendOrder import AmendOrder
from app.api.brokers.bybit.post.CancelAllOrers import CancelAllOrders
from app.api.brokers.bybit.post.CancelOrder import CancelOrder
from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.api.brokers.bybit.post.SetLeverage import SetLeverage
from app.api.brokers.bybit.models.get.OpenAndClosedOrdersAll import OpenAndClosedOrdersAll
from app.api.brokers.bybit.models.get.PositionInfoAll import PositionInfoAll
from app.api.brokers.bybit.models.post.CancelAllOrdersAll import CancelAllOrdersAll
from app.helper.registry.RateLimitRegistry import RateLimitRegistry
from app.mappers.ClassMapper import ClassMapper
from app.api.brokers.RequestParameters import RequestParameters

# endregion

rate_limit_registry = RateLimitRegistry(RateLimitEnum)

class BybitHandler:

    def __init__(self):
        self.name = "BYBIT"
        self.__broker: Bybit = Bybit("BYBIT")
        self.isLockActive = False
        self._bybitMapper = ClassMapper()
        self._rateLimitRegistry = RateLimitRegistry(RateLimitEnum)

    # region get Methods
    @rate_limit_registry.rate_limited
    def returnOpenAndClosedOrder(self,requestParams: RequestParameters) -> OpenAndClosedOrdersAll:

        openAndClosedOrders: OpenAndClosedOrders = (self._bybitMapper.map_args_to_dataclass
                                                    (OpenAndClosedOrders,requestParams,RequestParameters))


        # Validierung der Eingabeparameter
        if not openAndClosedOrders.validate():
            raise ValueError("The Fields that were required were not given")

        params = openAndClosedOrders.toQueryString()

        endPoint = EndPointEnum.OPENANDCLOSED.value
        method = "get"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], OpenAndClosedOrdersAll)

        return result

    @rate_limit_registry.rate_limited
    def returnPositionInfo(self,requestParams:RequestParameters) -> PositionInfoAll:

        positionInfo: PositionInfo = (self._bybitMapper.map_args_to_dataclass
                                      (PositionInfo,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not positionInfo.validate():
            raise ValueError("The Fields that were required were not given")

        params = positionInfo.toQueryString()

        endPoint = EndPointEnum.POSITIONINFO.value
        method = "get"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], PositionInfoAll)

        return result

    @rate_limit_registry.rate_limited
    def returnOrderHistory(self,requestParams: RequestParameters) -> OrderHistoryAll:

        orderHistory: OrderHistory = (self._bybitMapper.map_args_to_dataclass
                                                    (OrderHistory,requestParams,RequestParameters))


        # Validierung der Eingabeparameter
        if not orderHistory.validate():
            raise ValueError("The Fields that were required were not given")

        params = orderHistory.toQueryString()

        endPoint = EndPointEnum.HISTORY.value
        method = "get"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], OrderHistoryAll)

        return result

    # endregion

    # region post Methods
    @rate_limit_registry.rate_limited
    def amendOrder(self,requestParams:RequestParameters) -> ResponseParameters:
        amendOrder: AmendOrder = (self._bybitMapper.map_args_to_dataclass
                                  (AmendOrder,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = amendOrder.toDict()

        endPoint = EndPointEnum.AMEND.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], ResponseParameters)

        return result

    @rate_limit_registry.rate_limited
    def cancelAllOrders(self,requestParams:RequestParameters) -> CancelAllOrdersAll:

        cancelOrders: CancelAllOrders = (self._bybitMapper.map_args_to_dataclass
                                         (CancelAllOrders,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not cancelOrders.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrders.toDict()

        endPoint = EndPointEnum.CANCELALL.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], CancelAllOrdersAll)

        return result

    @rate_limit_registry.rate_limited
    def cancelOrder(self,requestParams:RequestParameters) -> ResponseParameters:
        cancelOrder: CancelOrder = (self._bybitMapper.map_args_to_dataclass
                                    (CancelOrder,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not cancelOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrder.toDict()

        endPoint = EndPointEnum.CANCEL.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], ResponseParameters)

        return result

    @rate_limit_registry.rate_limited
    def placeOrder(self,requestParams:RequestParameters) -> ResponseParameters:

        placeOrder: PlaceOrder = (self._bybitMapper.map_args_to_dataclass
                                  (PlaceOrder,requestParams,RequestParameters))

        # Validierung der Eingabeparameter
        if not placeOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = placeOrder.toDict()

        endPoint = EndPointEnum.PLACEORDER.value
        method = "post"

        responseJson = self.__broker.sendRequest(endPoint, method, params)
        result = self._bybitMapper.map_dict_to_dataclass(responseJson['result'], ResponseParameters)

        return result

    @rate_limit_registry.rate_limited
    def setLeverage(self,requestParams:RequestParameters) -> bool:
        setLeverage: SetLeverage = (self._bybitMapper.map_args_to_dataclass
                                    (SetLeverage,requestParams,RequestParameters))

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

    # endregion

    # todo Logic for Handling Failed Requests and Logging
    # todo adjust order to split tp and stop order testing

bh = BybitHandler()
request = RequestParameters()
request.category = "linear"
request.symbol = "XRPUSDT"
res = bh.returnOpenAndClosedOrder(request)
request.takeProfit =  "4"
# bh.amendOrder(request)
# print(res)