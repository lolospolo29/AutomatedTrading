import random
import string

from files.models.asset.Relation import Relation
from files.models.frameworks.FrameWork import FrameWork
from files.models.trade.Order import Order
from files.models.trade.enums.OrderType import OrderType


class OrderBuilder:
    def __init__(self):
        self.order = None  # Only create order when needed

    def create_order(self, relation:Relation, symbol:str, confirmations:list[FrameWork], category:str, side:str,
                     risk_percentage:float, order_number:int, tradeId:str, entry_frame_work:
                     FrameWork=None, qty=None):
        self.order = Order()
        o = self.order
        o.tradeId = tradeId
        orderlinkId = self._generate_order_link_id(relation.asset, relation.broker,
                                                   relation.strategy, order_number)
        o.order_link_id = orderlinkId
        o.confirmations = confirmations
        o.entry_frame_work = entry_frame_work
        o.symbol = symbol
        o.category = category
        o.side = side
        o.money_at_risk = 0.0
        o.risk_percentage = risk_percentage
        o.order_type = OrderType.MARKET.value # set Default
        if qty is not None:
            o.qty = qty
        return self

    def set_defaults(self,price:str=None, time_in_force:str=None, take_profit:str=None,
                     stop_loss:str=None, reduce_only:bool=None, close_on_trigger:bool=None):
        order = self.order
        if price is not None:
            order.price = price
        if time_in_force is not None:
            order.time_in_force = time_in_force
        if take_profit is not None:
            order.take_profit = take_profit
        if stop_loss is not None:
            order.stop_loss = stop_loss
        if reduce_only is not None:
            order.reduce_only = reduce_only
        if close_on_trigger is not None:
            order.close_on_trigger = close_on_trigger
        return self

    def set_spot(self, is_leverage:str=None, market_unit:str=None, orderlv:str=None):
        order = self.order
        if is_leverage is not None:
            order.is_leverage = is_leverage
        if market_unit is not None:
            order.market_unit = market_unit
        if orderlv is not None:
            order.orderlv = orderlv
        return self

    def set_conditional(self, trigger_price:str=None, trigger_by:str=None,
                        tp_trigger_by:str=None, sl_trigger_by:str=None,
                        trigger_direction:int=None):
        order = self.order
        if trigger_price is not None:
            order.trigger_price = trigger_price
        if trigger_by is not None:
            order.trigger_by = trigger_by
        if tp_trigger_by is not None:
            order.tp_trigger_by = tp_trigger_by
        if sl_trigger_by is not None:
            order.sl_trigger_by = sl_trigger_by
        if trigger_direction is not None:
            order.trigger_direction = trigger_direction
        return self

    def set_limit(self, tpsl_mode:str=None, tp_limit_price:str=None, sl_limit_price:str=None,
                  tp_order_type:str=None, sl_order_type:str=None):
        order = self.order
        if tpsl_mode is not None:
            order.tpsl_mode = tpsl_mode
        if tp_limit_price is not None:
            order.tp_limit_price = tp_limit_price
        if sl_limit_price is not None:
            order.sl_limit_price = sl_limit_price
        if tp_order_type is not None:
            order.tp_order_type = tp_order_type
        if sl_order_type is not None:
            order.sl_order_type = sl_order_type
        order.order_type = OrderType.LIMIT.value
        return self

    def build(self):
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
