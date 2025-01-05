# region Imports

from app.api.ResponseParams import ResponseParams
from app.api.brokers.bybit.Bybit import Bybit
from app.api.brokers.bybit.BybitMapper import BybitMapper
from app.api.brokers.bybit.enums.EndPointEnum import EndPointEnum
from app.api.brokers.bybit.enums.OpenOnlyEnum import OpenOnlyEnum
from app.api.brokers.bybit.enums.OrderFilterEnum import OrderFilterEnum
from app.api.brokers.bybit.enums.RateLimitEnum import RateLimitEnum
from app.api.brokers.bybit.get.OpenAndClosedOrders import OpenAndClosedOrders
from app.api.brokers.bybit.get.PostionInfo import PositionInfo
from app.api.brokers.bybit.post.AddOrReduceMargin import AddOrReduceMargin
from app.api.brokers.bybit.post.AmendOrder import AmendOrder
from app.api.brokers.bybit.post.CancelAllOrers import CancelAllOrders
from app.api.brokers.bybit.post.CancelOrder import CancelOrder
from app.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from app.api.brokers.bybit.post.SetLeverage import SetLeverage
from app.api.brokers.bybit.reponse.get.OpenAndClosedOrdersAll import OpenAndClosedOrdersAll
from app.api.brokers.bybit.reponse.get.PositionInfoAll import PositionInfoAll
from app.api.brokers.bybit.reponse.post.AddOrReduceMarginAll import AddOrReduceMarginAll
from app.api.brokers.bybit.reponse.post.AmendOrderAll import AmendOrderAll
from app.api.brokers.bybit.reponse.post.CancelAllOrdersAll import CancelAllOrdersAll
from app.api.brokers.bybit.reponse.post.CancelOrderAll import CancelOrderAll
from app.api.brokers.bybit.reponse.post.PlaceOrderAll import PlaceOrderAll
from app.helper.registry.RateLimitRegistry import RateLimitRegistry
from app.models.trade.CategoryEnum import CategoryEnum
from app.models.trade.Order import Order
from app.models.trade.OrderDirectionEnum import OrderDirection
from app.models.trade.OrderTypeEnum import OrderTypeEnum

# endregion

rate_limit_registry = RateLimitRegistry(RateLimitEnum)

class BybitHandler:

    def __init__(self):
        self.name = "bybit"
        self.__broker: Bybit = Bybit("bybit")
        self._bybitMapper = BybitMapper()
        self.isLockActive = False
        self._rateLimitRegistry = RateLimitRegistry(RateLimitEnum)

    # region get Methods
    @rate_limit_registry.rate_limited
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

    @rate_limit_registry.rate_limited
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

    # endregion

    # region post Methods
    @rate_limit_registry.rate_limited
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

    @rate_limit_registry.rate_limited
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

    @rate_limit_registry.rate_limited
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

    @rate_limit_registry.rate_limited
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

    @rate_limit_registry.rate_limited
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

    @rate_limit_registry.rate_limited
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
    # endregion

    # Logic for Handling Failed Requests and Logging
