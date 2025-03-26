from typing import Optional

from files.models.asset.Relation import Relation
from files.models.broker.RequestParameters import RequestParameters
from files.models.trade.Order import Order


class RequestBuilder:
    def __init__(self):
        self.request: Optional[RequestParameters] = None

    def create_request(self) -> "RequestBuilder":
        """Initialize a new request."""
        self.request = RequestParameters(brokerId="")  # brokerId is required
        return self

    def add_order(self, order: Order) -> "RequestBuilder":
        """Add order details to request."""
        if not self.request:
            raise ValueError("Request not initialized. Call create_request() first.")

        self.request.orderId = order.order_id
        self.request.orderLinkId = order.order_link_id
        self.request.orderType = order.order_type
        self.request.symbol = order.symbol
        self.request.category = order.category
        self.request.side = order.side
        self.request.qty = order.qty
        self.request.price = order.price
        self.request.timeInForce = order.time_in_force
        self.request.reduceOnly = order.reduce_only
        self.request.closeOnTrigger = order.close_on_trigger
        self.request.triggerPrice = order.trigger_price
        self.request.triggerBy = order.trigger_by
        self.request.tpTriggerBy = order.tp_trigger_by
        self.request.slTriggerBy = order.sl_trigger_by
        self.request.triggerDirection = order.trigger_direction
        self.request.tpslMode = order.tpsl_mode
        self.request.tpLimitPrice = order.tp_limit_price
        self.request.tpOrderType = order.tp_order_type
        self.request.slOrderType = order.sl_order_type
        self.request.slLimitPrice = order.sl_limit_price
        self.request.stopLoss = order.stop_loss
        self.request.takeProfit = order.take_profit
        self.request.isLeverage = order.is_leverage
        self.request.marketUnit = order.market_unit
        return self

    def add_relation(self, relation: Relation) -> "RequestBuilder":
        """Add relation details to request."""
        if not self.request:
            raise ValueError("Request not initialized. Call create_request() first.")

        self.request.brokerId = str(relation.broker_id)
        self.request.category = str(relation.category_id) if relation.category_id else None
        return self

    def build(self) -> RequestParameters:
        """Return the built request."""
        if not self.request:
            raise ValueError("Request not initialized. Call create_request() first.")
        return self.request

