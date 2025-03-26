# region Imports
import time
from typing import Optional
from urllib.parse import urlencode

from logging import Logger

from files.api.brokers.bybit.Bybit import Bybit
from files.api.brokers.bybit.enums.EndPoint import EndPointEnum
from files.api.brokers.bybit.get.FundingHistory import FundingHistory
from files.api.brokers.bybit.get.OpenAndClosedOrders import OpenAndClosedOrders
from files.api.brokers.bybit.get.OrderHistory import OrderHistory
from files.api.brokers.bybit.get.PostionInfo import PositionInfo
from files.api.brokers.bybit.post.AmendOrder import AmendOrder
from files.api.brokers.bybit.post.CancelAllOrers import CancelAllOrders
from files.api.brokers.bybit.post.CancelOrder import CancelOrder
from files.api.brokers.bybit.post.PlaceOrder import PlaceOrder
from files.api.brokers.bybit.post.SetLeverage import SetLeverage
from files.models.broker.BrokerFunding import BrokerFunding
from files.models.broker.BrokerOrder import BrokerOrder
from files.models.broker.BrokerPosition import BrokerPosition
from files.interfaces.IBrokerHandler import IBrokerHandler
from files.helper.mappers.ClassMapper import ClassMapper
from files.models.broker.RequestParameters import RequestParameters
from ratelimit import limits
# endregion

FIFTEEN_MINUTES = 2

class BybitHandler(IBrokerHandler):

    def __init__(self,bybit:Bybit,logger:Logger):
        self._name = "BYBIT"
        self._broker: Bybit = bybit
        self._logger = logger

    @property
    def name(self) -> str:
        return self._name

    # region get Methods

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def return_open_and_closed_order(self, request_params: RequestParameters) -> list[BrokerOrder]:

        openAndClosedOrders: OpenAndClosedOrders = ClassMapper.map_source_to_target_model(request_params, OpenAndClosedOrders)

        self._logger.info(f"Open And Closed Orders Bybit,Symbol:{openAndClosedOrders.symbol}")

        if not openAndClosedOrders.validate():
            self._logger.error(f"Position Info Request Failed:{OrderHistory.symbol}")
            return []

        endPoint = EndPointEnum.OPENANDCLOSED.value
        method = "get"
        previousCursor: str = ""
        brokerOrderList: list[BrokerOrder] = []

        while True:

            funding_history_dict = openAndClosedOrders.model_dump()
            filtered_dict = {key: value for key, value in funding_history_dict.items() if value is not None}
            params = urlencode(filtered_dict)

            responseJson = self._broker.send_request(endPoint, method, params)
            if not responseJson.get("retMsg") == "OK":
                self._logger.error(f"Position Info Request Failed:{OrderHistory.symbol}")
                return []

            objList = responseJson.get("result").get("list")
            category = responseJson.get("result").get("category")
            nextPageCursor: str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
                bo: BrokerOrder = BrokerOrder.model_validate(obj)
                bo.category = category
                brokerOrderList.append(bo)

            time.sleep(1)
            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            openAndClosedOrders.cursor = nextPageCursor
        return brokerOrderList

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def return_position_info(self, request_params: RequestParameters) -> list[BrokerPosition]:
        positionInfo: PositionInfo = ClassMapper.map_source_to_target_model(request_params, PositionInfo)

        self._logger.info(f"Position Info Bybit,Symbol:{request_params.symbol}")

        if not positionInfo.validate():
            self._logger.error(f"Position Info Validation Failed:{OrderHistory.symbol}")
            return []

        endPoint = EndPointEnum.POSITIONINFO.value
        method = "get"
        previousCursor: str = ""
        brokerPositionList: list[BrokerPosition] = []

        while True:

            funding_history_dict = positionInfo.model_dump()
            filtered_dict = {key: value for key, value in funding_history_dict.items() if value is not None}
            params = urlencode(filtered_dict)

            responseJson = self._broker.send_request(endPoint, method, params)
            if not responseJson.get("retMsg") == "OK":
                self._logger.error(f"Position Info Request Failed:{OrderHistory.symbol}")
                return []

            objList = responseJson.get("result").get("list")
            category = responseJson.get("result").get("category")
            nextPageCursor: str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
                pi: BrokerPosition = BrokerPosition.model_validate(obj)
                pi.category = category
                brokerPositionList.append(pi)

            time.sleep(1)
            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            positionInfo.cursor = nextPageCursor
        return brokerPositionList

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def return_order_history(self, request_params: RequestParameters) -> list[BrokerOrder]:
        orderHistory: OrderHistory = ClassMapper.map_source_to_target_model(request_params, OrderHistory)

        self._logger.info(f"Order History Bybit,Symbol:{orderHistory.symbol}")

        if not orderHistory.validate():
            self._logger.error(f"Order History Validation Failed:{OrderHistory.symbol}")
            return []

        endPoint = EndPointEnum.HISTORY.value
        method = "get"
        previousCursor: str = ""
        brokerOrderList: list[BrokerOrder] = []

        while True:

            funding_history_dict = orderHistory.model_dump()
            filtered_dict = {key: value for key, value in funding_history_dict.items() if value is not None}
            params = urlencode(filtered_dict)

            responseJson = self._broker.send_request(endPoint, method, params)
            if not responseJson.get("retMsg") == "OK":
                self._logger.error(f"Order History Validation Failed:{OrderHistory.symbol}")
                return []

            objList = responseJson.get("result").get("list")
            category = responseJson.get("result").get("category")
            nextPageCursor: str = responseJson.get("result").get("nextPageCursor")

            for obj in objList:
                bo: BrokerOrder = BrokerOrder.model_validate(obj)
                bo.category = category
                brokerOrderList.append(bo)

            time.sleep(1)
            if nextPageCursor == previousCursor or nextPageCursor == "":
                break

            previousCursor = nextPageCursor
            orderHistory.cursor = nextPageCursor
        return brokerOrderList

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def return_funding_history(self, request_params: RequestParameters) -> list[BrokerFunding]:
        fundingHistory: FundingHistory = ClassMapper.map_source_to_target_model(request_params, FundingHistory)

        self._logger.info(f"Sending API-Call to Return Funding History  Bybit,Symbol:{request_params.symbol}")

        if not fundingHistory.validate():
            self._logger.error(f"Funding History Validation Failed:{fundingHistory.symbol}")
            return []

        endPoint = EndPointEnum.FUNDING.value
        method = "get"
        funding_history_dict = fundingHistory.model_dump()
        filtered_dict = {key: value for key, value in funding_history_dict.items() if value is not None}
        params = urlencode(filtered_dict)
        brokeFundingList: list[BrokerFunding] = []

        responseJson = self._broker.send_request(endPoint, method, params)
        if not responseJson.get("retMsg") == "OK":
            self._logger.error(f"Funding History Request Failed:{fundingHistory.symbol}")
            return []

        objList = responseJson.get("result").get("list")
        category = responseJson.get("result").get("category")

        for obj in objList:
            bf: BrokerFunding = BrokerFunding.model_validate(obj)
            bf.category = category
            brokeFundingList.append(bf)

        return brokeFundingList

    # endregion

    # region post Methods
    @limits(calls=10, period=FIFTEEN_MINUTES)
    def amend_order(self, request_params: RequestParameters) -> Optional[BrokerOrder]:
        amendOrder: AmendOrder = ClassMapper.map_source_to_target_model(request_params, AmendOrder)

        self._logger.info(f"Amend Order Bybit,OrderLinkId:{request_params.orderLinkId},{request_params.symbol}")

        if not amendOrder.validate():
            self._logger.error(f"Amend Order Validation Failed:{amendOrder.orderLinkId}")
            return

        params = amendOrder.model_dump_json()
        endPoint = EndPointEnum.AMEND.value
        method = "post"

        responseJson = self._broker.send_request(endPoint, method, params)
        if not responseJson.get("retMsg") == "OK":
            self._logger.error(f"Amend Order Request Failed:{amendOrder.orderLinkId}")
            return

        result:BrokerOrder = BrokerOrder.model_validate(responseJson['result'])
        return result

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def cancel_all_orders(self, request_params: RequestParameters) -> list[BrokerOrder]:
        cancelOrders: CancelAllOrders = ClassMapper.map_source_to_target_model(request_params, CancelAllOrders)
        self._logger.info(f"Sending API-Call to Cancel All Orders Bybit,Symbol:{request_params.symbol}")

        if not cancelOrders.validate():
            self._logger.error(f"Cancell Orders Validation Failed:{cancelOrders}")
            return []

        endPoint = EndPointEnum.CANCELALL.value
        method = "post"
        params = cancelOrders.model_dump_json()
        brokerOrderList: list[BrokerOrder] = []

        responseJson = self._broker.send_request(endPoint, method, params)
        if not responseJson.get("retMsg") == "OK":
            self._logger.error(f"Cancell Orders Request Failed:{cancelOrders}")
            return []

        objList = responseJson.get("result").get("list")

        for obj in objList:
            brokerOrderList.append(BrokerOrder.model_validate(obj))
        return brokerOrderList

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def cancel_order(self, request_params: RequestParameters) -> Optional[BrokerOrder]:
        cancelOrder: CancelOrder = ClassMapper.map_source_to_target_model(request_params, CancelOrder)

        self._logger.info(f"Cancel Order To Bybit,OrderLinkId:{request_params.orderLinkId},{request_params.symbol}")

        if not cancelOrder.validate():
            self._logger.error(f"Cancel Order Validation Failed:{cancelOrder.orderLinkId}")
            return

        params = cancelOrder.model_dump_json()
        endPoint = EndPointEnum.CANCEL.value
        method = "post"

        responseJson = self._broker.send_request(endPoint, method, params)
        if not responseJson.get("retMsg") == "OK":
            self._logger.error(f"Cancel Order Request Failed:{cancelOrder.orderLinkId}")
            return

        result = BrokerOrder.model_validate(responseJson['result'])
        return result

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def place_order(self, request_params: RequestParameters) -> Optional[BrokerOrder]:
        placeOrder: PlaceOrder = ClassMapper.map_source_to_target_model(request_params, PlaceOrder)

        self._logger.info(f"Place Order Bybit,OrderLinkId:{request_params.orderLinkId},{request_params.symbol}")

        if not placeOrder.validate():
            self._logger.error(f"Place Order Validation Failed:{placeOrder.orderLinkId}")
            return

        params = placeOrder.model_dump_json()
        endPoint = EndPointEnum.PLACEORDER.value
        method = "post"

        responseJson = self._broker.send_request(endPoint, method, params)
        if not responseJson.get("retMsg") == "OK":
            self._logger.error(f"Place Order Request Failed:{placeOrder.orderLinkId}")
            return

        result = BrokerOrder.model_validate(responseJson["result"])
        return result

    @limits(calls=10, period=FIFTEEN_MINUTES)
    def set_leverage(self, request_params: RequestParameters) -> Optional[bool]:
        setLeverage: SetLeverage = ClassMapper.map_source_to_target_model(request_params, SetLeverage)

        self._logger.info(f"Set Leverage Bybit,OrderLinkId:{request_params.orderLinkId},{request_params.symbol}")

        if not setLeverage.validate():
            self._logger.error(f"Set Leverage Validation Failed:{setLeverage.symbol}")
            return

        params = setLeverage.model_dump_json()
        endPoint = EndPointEnum.SETLEVERAGE.value
        method = "post"

        responseJson = self._broker.send_request(endPoint, method, params)
        if not responseJson.get("retMsg") == "OK":
            self._logger.error(f"Set Leverage Request Failed:{setLeverage.symbol}")
            return

        # Use retry utility to handle retries
        return responseJson["retMsg"] == "OK"

    # endregion
