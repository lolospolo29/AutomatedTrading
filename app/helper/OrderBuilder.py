from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.frameworks.FrameWork import FrameWork
from app.models.trade.Order import Order
from app.models.trade.OrderDirectionEnum import OrderDirection
from app.models.trade.OrderTypeEnum import OrderTypeEnum
from app.models.trade.TPSLModeEnum import TPSLModeEnum
from app.models.trade.TimeInForceEnum import TimeInForceEnum
from app.models.trade.TriggerByEnum import TriggerByEnum
from app.models.trade.TriggerDirectionEnum import TriggerDirection


class OrderBuilder:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OrderBuilder, cls).__new__(cls)
        return cls._instance

    def createOrder(self,assetBrokerStrategyRelation:AssetBrokerStrategyRelation,entryFrameWork:
    FrameWork, symbol:str,confirmations:list[FrameWork], category:str, side:OrderDirection,
                    riskPercentage:float,orderNumber:int)->Order:
        o = Order()
        orderlinkId = self._generate_order_link_id(assetBrokerStrategyRelation.asset,assetBrokerStrategyRelation.broker,
                                     assetBrokerStrategyRelation.strategy,orderNumber)
        o.orderlinkId = orderlinkId
        o.confirmations = confirmations
        o.entryFrameWork = entryFrameWork
        o.symbol = symbol
        o.category = category
        o.side = side.value
        o.moneyAtRisk = 0.0
        o.unrealizedProfit = 0.0
        o.riskPercentage = riskPercentage
        o.orderType = OrderTypeEnum.MARKET.value # set Default
        return o

    @staticmethod
    def setDefaults(order: Order,price:str=None,timeInForce:TimeInForceEnum=None,takeProfit:str=None,
                    stopLoss:str=None,reduceOnly:bool=None,closeOnTrigger:bool=None)->Order:
        if price is not None:
            order.price = price
        if timeInForce is not None:
            order.timeInForce = timeInForce.value
        if takeProfit is not None:
            order.takeProfit = takeProfit
        if stopLoss is not None:
            order.stopLoss = stopLoss
        if reduceOnly is not None:
            order.reduceOnly = reduceOnly
        if closeOnTrigger is not None:
            order.closeOnTrigger = closeOnTrigger
        return order

    @staticmethod
    def setSpot(order: Order,isLeverage:bool=None,marketUnit:str=None,orderFilter:str=None,orderlv:str=None)->Order:
        if isLeverage is not None:
            order.isLeverage = isLeverage
        if marketUnit is not None:
            order.marketUnit = marketUnit
        if orderFilter is not None:
            order.orderFilter = orderFilter
        if orderlv is not None:
            order.orderlv = orderlv
        return order

    @staticmethod
    def setConditional(order: Order,triggerPrice:str=None,triggerBy:TriggerByEnum=None,
                            tpTriggerBy:TriggerByEnum=None,slTriggerBy:TriggerByEnum=None,
                            triggerDirection:TriggerDirection=None)->Order:
        if triggerPrice is not None:
            order.triggerPrice = triggerPrice
        if triggerBy is not None:
            order.triggerBy = triggerBy.value
        if tpTriggerBy is not None:
            order.tpTriggerBy = tpTriggerBy.value
        if slTriggerBy is not None:
            order.slTriggerBy = slTriggerBy.value
        if triggerDirection is not None:
            order.triggerDirection = triggerDirection.value
        order.orderType = OrderTypeEnum.LIMIT.value
        return order

    @staticmethod
    def setLimit(order:Order,tpslMode:TPSLModeEnum=None,tpLimitPrice:str=None,slLimitPrice:str=None,
                 tpOrderType:OrderTypeEnum=None,slOrderType:OrderTypeEnum=None)->Order:
        if tpslMode is not None:
            order.tpslMode = tpslMode.value
        if tpLimitPrice is not None:
            order.tpLimitPrice = tpLimitPrice
        if slLimitPrice is not None:
            order.slLimitPrice = slLimitPrice
        if tpOrderType is not None:
            order.tpOrderType = tpOrderType.value
        if slOrderType is not None:
            order.slOrderType = slOrderType.value
        if tpOrderType is not None:
            order.tpOrderType = tpOrderType.value
        return order


    @staticmethod
    def _generate_order_link_id(asset: str, broker: str, strategy: str, order_number: int) -> str:
        """
        Generate a custom orderLinkId with the format:
        yymmddhhmmss-<3_letters_currency>-<3_letters_broker>-<3_letters_strategy>-<order_number>

        Args:
            asset (str): The currency name (e.g., "Bitcoin").
            broker (str): The broker name (e.g., "Binance").
            strategy (str): The strategy name (e.g., "Scalping").
            order_number (int): The order number (e.g., 1).

        Returns:
            str: A formatted orderLinkId.
        """
        from datetime import datetime
        # Current timestamp in the format yymmddhhmmss
        timestamp = datetime.now().strftime("%y%m%d%H%M%S")

        # Take the first 3 letters of the input values, converted to uppercase
        currency_part = asset[:3].upper()
        broker_part = broker[:3].upper()
        strategy_part = strategy[:3].upper()

        # Format the orderLinkId
        order_link_id = f"{timestamp}-{currency_part}-{broker_part}-{strategy_part}-{order_number:03}"

        return order_link_id

