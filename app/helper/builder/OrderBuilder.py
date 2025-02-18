import random
import string

from app.models.asset.Relation import Relation
from app.models.frameworks.FrameWork import FrameWork
from app.models.strategy.OrderResultStatusEnum import OrderResultStatusEnum
from app.models.trade.Order import Order
from app.models.trade.enums.OrderTypeEnum import OrderTypeEnum
from app.monitoring.logging.logging_startup import logger


class OrderBuilder:
    def __init__(self):
        self.order = Order()

    def create_order(self, relation:Relation, symbol:str, confirmations:list[FrameWork], category:str, side:str,
                     risk_percentage:float, order_number:int, tradeId:str, entry_frame_work:
                     FrameWork=None, qty=None):
        o = self.order
        o.tradeId = tradeId
        orderlinkId = self._generate_order_link_id(relation.asset, relation.broker,
                                                   relation.strategy, order_number)
        o.orderLinkId = orderlinkId
        o.confirmations = confirmations
        o.entry_frame_work = entry_frame_work
        o.symbol = symbol
        o.category = category
        o.side = side
        o.money_at_risk = 0.0
        o.risk_percentage = risk_percentage
        o.order_result_status = OrderResultStatusEnum.NEW.value
        o.orderType = OrderTypeEnum.MARKET.value # set Default
        if qty is not None:
            o.qty = qty
        logger.debug(f"Building Order, OrderLinkId:{o.orderLinkId}, Symbol:{o.symbol},TradeId:{o.tradeId}")
        return self

    def set_defaults(self,price:str=None, time_in_force:str=None, take_profit:str=None,
                     stop_loss:str=None, reduce_only:bool=None, close_on_trigger:bool=None):
        order = self.order
        if price is not None:
            order.price = price
        if time_in_force is not None:
            order.timeInForce = time_in_force
        if take_profit is not None:
            order.takeProfit = take_profit
        if stop_loss is not None:
            order.stopLoss = stop_loss
        if reduce_only is not None:
            order.reduceOnly = reduce_only
        if close_on_trigger is not None:
            order.closeOnTrigger = close_on_trigger
        return self

    def set_spot(self, is_leverage:str=None, market_unit:str=None, orderlv:str=None):
        order = self.order
        if is_leverage is not None:
            order.isLeverage = is_leverage
        if market_unit is not None:
            order.marketUnit = market_unit
        if orderlv is not None:
            order.orderlv = orderlv
        return self

    def set_conditional(self, trigger_price:str=None, trigger_by:str=None,
                        tp_trigger_by:str=None, sl_trigger_by:str=None,
                        trigger_direction:int=None):
        order = self.order
        if trigger_price is not None:
            order.triggerPrice = trigger_price
        if trigger_by is not None:
            order.triggerBy = trigger_by
        if tp_trigger_by is not None:
            order.tpTriggerBy = tp_trigger_by
        if sl_trigger_by is not None:
            order.slTriggerBy = sl_trigger_by
        if trigger_direction is not None:
            order.triggerDirection = trigger_direction
        return self

    def set_limit(self, tpsl_mode:str=None, tp_limit_price:str=None, sl_limit_price:str=None,
                  tp_order_type:str=None, sl_order_type:str=None):
        order = self.order
        if tpsl_mode is not None:
            order.tpslMode = tpsl_mode
        if tp_limit_price is not None:
            order.tpLimitPrice = tp_limit_price
        if sl_limit_price is not None:
            order.slLimitPrice = sl_limit_price
        if tp_order_type is not None:
            order.tpOrderType = tp_order_type
        if sl_order_type is not None:
            order.slOrderType = sl_order_type
        if tp_order_type is not None:
            order.tpOrderType = tp_order_type
        order.orderType = OrderTypeEnum.LIMIT.value
        return self

    def build(self):
        logger.info(f"Order Build successfully, OrderLinkId: {self.order.orderLinkId},Symbol: {self.order.symbol},TradeId: {self.order.tradeId}")
        return self.order

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
