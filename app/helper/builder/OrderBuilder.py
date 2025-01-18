import string
import random

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.calculators.frameworks.FrameWork import FrameWork
from app.models.trade.enums.CategoryEnum import CategoryEnum
from app.models.trade.Order import Order
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.models.trade.enums.OrderStatusEnum import OrderStatusEnum
from app.models.trade.enums.OrderTypeEnum import OrderTypeEnum
from app.models.trade.enums.TPSLModeEnum import TPSLModeEnum
from app.models.trade.enums.TimeInForceEnum import TimeInForceEnum
from app.models.trade.enums.TriggerByEnum import TriggerByEnum
from app.models.trade.enums.TriggerDirectionEnum import TriggerDirection


class OrderBuilder:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OrderBuilder, cls).__new__(cls)
        return cls._instance


    def create_order(self, relation:AssetBrokerStrategyRelation, entry_frame_work:
    FrameWork, symbol:str, confirmations:list[FrameWork], category:CategoryEnum, side:OrderDirectionEnum,
                     risk_percentage:float, order_number:int, trade_id:str)->Order:
        o = Order()
        o.trade_id = trade_id
        orderlinkId = self._generate_order_link_id(relation.asset, relation.broker,
                                                   relation.strategy, order_number)
        o.orderlinkId = orderlinkId
        o.confirmations = confirmations
        o.entry_frame_work = entry_frame_work
        o.symbol = symbol
        o.category = category.value
        o.side = side.value
        o.money_at_risk = 0.0
        o.unrealizedProfit = 0.0
        o.risk_percentage = risk_percentage
        o.orderType = OrderTypeEnum.MARKET.value # set Default
        return o

    @staticmethod
    def set_defaults(order: Order, price:str=None, time_in_force:TimeInForceEnum=None, take_profit:str=None,
                     stop_loss:str=None, reduce_only:bool=None, close_on_trigger:bool=None)->Order:
        if price is not None:
            order.price = price
        if time_in_force is not None:
            order.timeInForce = time_in_force.value
        if take_profit is not None:
            order.takeProfit = take_profit
        if stop_loss is not None:
            order.stopLoss = stop_loss
        if reduce_only is not None:
            order.reduceOnly = reduce_only
        if close_on_trigger is not None:
            order.closeOnTrigger = close_on_trigger
        return order

    @staticmethod
    def set_spot(order: Order, is_leverage:bool=None, market_unit:str=None, order_filter:str=None, orderlv:str=None)->Order:
        if is_leverage is not None:
            order.isLeverage = is_leverage
        if market_unit is not None:
            order.marketUnit = market_unit
        if order_filter is not None:
            order.orderFilter = order_filter
        if orderlv is not None:
            order.orderlv = orderlv
        return order

    @staticmethod
    def set_conditional(order: Order, trigger_price:str=None, trigger_by:TriggerByEnum=None,
                        tp_trigger_by:TriggerByEnum=None, sl_trigger_by:TriggerByEnum=None,
                        trigger_direction:TriggerDirection=None)->Order:
        if trigger_price is not None:
            order.triggerPrice = trigger_price
        if trigger_by is not None:
            order.triggerBy = trigger_by.value
        if tp_trigger_by is not None:
            order.tpTriggerBy = tp_trigger_by.value
        if sl_trigger_by is not None:
            order.slTriggerBy = sl_trigger_by.value
        if trigger_direction is not None:
            order.triggerDirection = trigger_direction.value
        order.orderType = OrderTypeEnum.LIMIT.value
        return order

    @staticmethod
    def set_limit(order:Order, tpsl_mode:TPSLModeEnum=None, tp_limit_price:str=None, sl_limit_price:str=None,
                  tp_order_type:OrderTypeEnum=None, sl_order_type:OrderTypeEnum=None)->Order:
        if tpsl_mode is not None:
            order.tpslMode = tpsl_mode.value
        if tp_limit_price is not None:
            order.tpLimitPrice = tp_limit_price
        if sl_limit_price is not None:
            order.slLimitPrice = sl_limit_price
        if tp_order_type is not None:
            order.tpOrderType = tp_order_type.value
        if sl_order_type is not None:
            order.slOrderType = sl_order_type.value
        if tp_order_type is not None:
            order.tpOrderType = tp_order_type.value
        order.orderType = OrderTypeEnum.LIMIT.value
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

        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=7))

        # Format the orderLinkId
        order_link_id = f"{timestamp}-{currency_part}-{broker_part}-{strategy_part}-{order_number:03}-{random_part}"

        return order_link_id
