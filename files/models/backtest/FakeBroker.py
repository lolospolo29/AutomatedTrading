from random import random

from files.models.asset.Candle import Candle
from files.models.trade.Order import Order
from files.models.trade.enums.Side import Side
from files.models.trade.enums.OrderType import OrderType
from files.models.trade.enums.TriggerDirection import TriggerDirection


class FakeBroker:

    @staticmethod
    def get_execution_price(last_candle, order_side)->float:
        """
        Simulate market order execution price with potential slippage.
        """
        slippage_pct = random.uniform(0, 0.00045)  # Example: Up to 0.05% slippage

        if order_side == Side.BUY.value:
            return last_candle.low * (1 + slippage_pct)  # Buy fills slightly higher
        elif order_side == Side.SELL.value:
            return last_candle.high * (1 - slippage_pct)  # Sell fills slightly lower
        return last_candle.close  # Default to last price if no slippage

    @staticmethod
    def check_conditional_order(trigger_direction:int,trigger_price:float, last_candle: Candle)->bool:
        if trigger_direction:
            if trigger_direction == TriggerDirection.FALL.value and last_candle.low <= trigger_price:
                return True

            if trigger_direction == TriggerDirection.RISE.value and last_candle.high >= trigger_price:
                return True
        return False

    @staticmethod
    def create_limit_exit_order(order:Order, is_stop:bool)->Order:
        o = Order()
        o.order_type = OrderType.LIMIT.value
        o.order_id = order.order_id + str(random.randint(1, 10000))
        o.qty = order.qty
        if not is_stop:
            o.price = order.tp_limit_price
        if is_stop:
            o.price = order.sl_limit_price

        if order.side == Side.BUY.value:
            o.side = Side.SELL.value
        if order.side == Side.SELL.value:
            o.side = Side.BUY.value
        return o

    @staticmethod
    def create_market_exit_order(order:Order, is_stop:bool)->Order:
        o = Order()
        o.order_type = OrderType.MARKET.value
        o.order_id = order.order_id + str(random.randint(1, 10000))
        o.qty = order.qty
        if not is_stop:
            o.trigger_price = order.take_profit
        if is_stop:
            o.trigger_price = order.stop_loss

        if order.side == Side.BUY.value:
            o.side = Side.SELL.value
        if order.side == Side.SELL.value:
            o.side = Side.BUY.value
        return o

    def create_tp_sl_order(self, order:Order)->list[Order]:
        new_orders = []
        if order.take_profit:
            if order.tp_limit_price:
                limit_order:Order = self.create_limit_exit_order(order=order, is_stop=False)
                new_orders.append(limit_order)
            else:
                market_order:Order = self.create_market_exit_order(order=order, is_stop=False)
                new_orders.append(market_order)
        if order.stop_loss:
            if order.sl_limit_price:
                limit_order:Order = self.create_limit_exit_order(order=order, is_stop=True)
                new_orders.append(limit_order)
            else:
                market_order:Order = self.create_market_exit_order(order=order, is_stop=True)
                new_orders.append(market_order)
        return new_orders