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
from app.monitoring.retry_request import retry_request

# endregion

rate_limit_registry = RateLimitRegistry(RateLimitEnum)

class BybitHandler(IBrokerHandler):

    def __init__(self):
        self.name = "BYBIT"
        self.__broker: Bybit = Bybit("BYBIT")
        self.__is_lock_active = False
        self._class_mapper = ClassMapper()
        self._rate_limit_registry = RateLimitRegistry(RateLimitEnum)


    # region get Methods
    @rate_limit_registry.rate_limited
    def return_open_and_closed_order(self, request_params: RequestParameters) -> list[BrokerOrder]:

        openAndClosedOrders: OpenAndClosedOrders = (self._class_mapper.map_args_to_dataclass
                                                   (OpenAndClosedOrders, request_params, RequestParameters))


        # Validierung der Eingabeparameter
        if not openAndClosedOrders.validate():
            raise ValueError("The Fields that were required were not given")


        endPoint = EndPointEnum.OPENANDCLOSED.value
        method = "get"

        brokerOrderList: list[BrokerOrder] = []
        previousCursor:str = ""

        while True:

            params = openAndClosedOrders.to_query_string()
            responseJson = self.__broker.send_request(endPoint, method, params)

            objList = responseJson.get("result").get("list")
            nextPageCursor:str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
               brokerOrderList.append(self._class_mapper.map_dict_to_dataclass(obj, BrokerOrder))

            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            openAndClosedOrders.cursor = nextPageCursor

        return brokerOrderList

    @rate_limit_registry.rate_limited
    def return_position_info(self, request_params:RequestParameters) -> list[BrokerPosition]:

        positionInfo: PositionInfo = (self._class_mapper.map_args_to_dataclass
                                      (PositionInfo, request_params, RequestParameters))

        # Validierung der Eingabeparameter
        if not positionInfo.validate():
            raise ValueError("The Fields that were required were not given")


        endPoint = EndPointEnum.POSITIONINFO.value
        method = "get"

        brokerPositionList: list[BrokerPosition] = []
        previousCursor:str = ""

        while True:

            params = positionInfo.to_query_string()
            responseJson = self.__broker.send_request(endPoint, method, params)

            objList = responseJson.get("result").get("list")
            nextPageCursor:str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
               brokerPositionList.append(self._class_mapper.map_dict_to_dataclass(obj, BrokerPosition))

            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            positionInfo.cursor = nextPageCursor


        return brokerPositionList

    @rate_limit_registry.rate_limited
    def return_order_history(self, request_params: RequestParameters) -> list[BrokerOrder]:

        orderHistory: OrderHistory = (self._class_mapper.map_args_to_dataclass
                                                    (OrderHistory, request_params, RequestParameters))


        # Validierung der Eingabeparameter
        if not orderHistory.validate():
            raise ValueError("The Fields that were required were not given")

        endPoint = EndPointEnum.HISTORY.value
        method = "get"

        brokerOrderList: list[BrokerOrder] = []
        previousCursor:str = ""

        while True:

            params = orderHistory.to_query_string()
            responseJson = self.__broker.send_request(endPoint, method, params)

            objList = responseJson.get("result").get("list")
            nextPageCursor:str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
                brokerOrderList.append(self._class_mapper.map_dict_to_dataclass(obj, BrokerOrder))

            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            orderHistory.cursor = nextPageCursor

        return brokerOrderList

    # endregion

    # region post Methods
    @rate_limit_registry.rate_limited
    def amend_order(self, request_params:RequestParameters) -> BrokerOrder:
        amendOrder: AmendOrder = (self._class_mapper.map_args_to_dataclass
                                  (AmendOrder, request_params, RequestParameters))

        # Validierung der Eingabeparameter
        if not amendOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = amendOrder.to_dict()

        endPoint = EndPointEnum.AMEND.value
        method = "post"

        responseJson = self.__broker.send_request(endPoint, method, params)
        result = self._class_mapper.map_dict_to_dataclass(responseJson['result'], BrokerOrder)

        return result

    @rate_limit_registry.rate_limited
    def cancel_all_orders(self, request_params:RequestParameters) -> list[BrokerOrder]:

        cancelOrders: CancelAllOrders = (self._class_mapper.map_args_to_dataclass
                                         (CancelAllOrders, request_params, RequestParameters))

        # Validierung der Eingabeparameter
        if not cancelOrders.validate():
            raise ValueError("The Fields that were required were not given")

        endPoint = EndPointEnum.CANCELALL.value
        method = "post"

        params = cancelOrders.to_dict()

        brokerOrderList: list[BrokerOrder] = []

        responseJson = self.__broker.send_request(endPoint, method, params)

        objList = responseJson.get("result").get("list")

        for obj in objList:
            brokerOrderList.append(self._class_mapper.map_dict_to_dataclass(obj, BrokerOrder))

        return brokerOrderList

    @rate_limit_registry.rate_limited
    def cancel_order(self, request_params:RequestParameters) -> BrokerOrder:
        cancelOrder: CancelOrder = (self._class_mapper.map_args_to_dataclass
                                    (CancelOrder, request_params, RequestParameters))

        # Validierung der Eingabeparameter
        if not cancelOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = cancelOrder.to_dict()

        endPoint = EndPointEnum.CANCEL.value
        method = "post"

        responseJson = self.__broker.send_request(endPoint, method, params)
        result = self._class_mapper.map_dict_to_dataclass(responseJson['result'], BrokerOrder)

        return result

    @rate_limit_registry.rate_limited
    def place_order(self, request_params:RequestParameters) -> BrokerOrder:

        placeOrder: PlaceOrder = (self._class_mapper.map_args_to_dataclass
                                  (PlaceOrder, request_params, RequestParameters))

        # Validierung der Eingabeparameter
        if not placeOrder.validate():
            raise ValueError("The Fields that were required were not given")

        params = placeOrder.to_dict()

        endPoint = EndPointEnum.PLACEORDER.value
        method = "post"

        responseJson = self.__broker.send_request(endPoint, method, params)
        result = self._class_mapper.map_dict_to_dataclass(responseJson['result'], BrokerOrder)

        return result

    @rate_limit_registry.rate_limited
    def set_leverage(self, request_params:RequestParameters) -> bool:
        time.sleep(5)
        setLeverage: SetLeverage = (self._class_mapper.map_args_to_dataclass
                                    (SetLeverage, request_params, RequestParameters))

        # Validierung der Eingabeparameter
        if not setLeverage.validate():
            raise ValueError("The Fields that were required were not given")

        params = setLeverage.to_dict()

        endPoint = EndPointEnum.SETLEVERAGE.value
        method = "post"

        def request_function():
            """Encapsulated API request logic for retry utility."""
            responseJson = self.__broker.send_request(endPoint, method, params)
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
# bh.cancel_all_orders(request)

