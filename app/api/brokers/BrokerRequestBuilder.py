from app.api.brokers.models.RequestParameters import RequestParameters


class BrokerRequestBuilder:
    def __init__(self):
        self.request = RequestParameters()  # Initialize an empty RequestParameters object

    def set_broker(self, broker: str):
        self.request.broker = broker
        return self

    def set_position_idx(self, position_idx: int):
        self.request.positionIdx = position_idx
        return self

    def set_base_coin(self, base_coin: str):
        self.request.baseCoin = base_coin
        return self

    def set_settle_coin(self, settle_coin: str):
        self.request.settleCoin = settle_coin
        return self

    def set_open_only(self, open_only: str):
        self.request.openOnly = open_only
        return self

    def set_limit(self, limit: int):
        self.request.limit = limit
        return self

    def set_cursor(self, cursor: str):
        self.request.cursor = cursor
        return self

    def set_category(self, category: str):
        self.request.category = category
        return self

    def set_order_filter(self, order_filter: str):
        self.request.orderFilter = order_filter
        return self

    def set_stop_order_type(self, stop_order_type: bool):
        self.request.stopOrderType = stop_order_type
        return self

    def set_symbol(self, symbol: str):
        self.request.symbol = symbol
        return self

    def set_sell_leverage(self, sell_leverage: str):
        self.request.sellLeverage = sell_leverage
        return self

    def set_buy_leverage(self, buy_leverage: str):
        self.request.buyLeverage = buy_leverage
        return self

    def set_margin(self, margin: str):
        self.request.margin = margin
        return self

    def set_status(self, status: str):
        self.request.status = status
        return self

    def set_order_id(self, order_id: str):
        self.request.orderId = order_id
        return self

    def set_order_link_id(self, order_link_id: str):
        self.request.orderLinkId = order_link_id
        return self

    def set_exp_date(self, exp_date: str):
        self.request.expDate = exp_date
        return self

    def set_order_lv(self, order_lv: str):
        self.request.orderlv = order_lv
        return self

    def set_trigger_price(self, trigger_price: str):
        self.request.triggerPrice = trigger_price
        return self

    def set_price(self, price: str):
        self.request.price = price
        return self

    def set_tpsl_mode(self, tpsl_mode: str):
        self.request.tpslMode = tpsl_mode
        return self

    def set_take_profit(self, take_profit: str):
        self.request.takeProfit = take_profit
        return self

    def set_stop_loss(self, stop_loss: str):
        self.request.stopLoss = stop_loss
        return self

    def set_tp_trigger_by(self, tp_trigger_by: str):
        self.request.tpTriggerBy = tp_trigger_by
        return self

    def set_sl_trigger_by(self, sl_trigger_by: str):
        self.request.slTriggerBy = sl_trigger_by
        return self

    def set_trigger_by(self, trigger_by: str):
        self.request.triggerBy = trigger_by
        return self

    def set_tp_limit_price(self, tp_limit_price: str):
        self.request.tpLimitPrice = tp_limit_price
        return self

    def set_sl_limit_price(self, sl_limit_price: str):
        self.request.slLimitPrice = sl_limit_price
        return self

    def set_is_leverage(self, is_leverage: int):
        self.request.isLeverage = is_leverage
        return self

    def set_market_unit(self, market_unit: str):
        self.request.marketUnit = market_unit
        return self

    def set_trigger_direction(self, trigger_direction: int):
        self.request.triggerDirection = trigger_direction
        return self

    def set_time_in_force(self, time_in_force: str):
        self.request.timeInForce = time_in_force
        return self

    def set_reduce_only(self, reduce_only: bool):
        self.request.reduceOnly = reduce_only
        return self

    def set_close_on_trigger(self, close_on_trigger: bool):
        self.request.closeOnTrigger = close_on_trigger
        return self

    def set_smp_type(self, smp_type: str):
        self.request.smpType = smp_type
        return self

    def set_mmp(self, mmp: bool):
        self.request.mmp = mmp
        return self

    def set_tp_order_type(self, tp_order_type: str):
        self.request.tpOrderType = tp_order_type
        return self

    def set_sl_order_type(self, sl_order_type: str):
        self.request.slOrderType = sl_order_type
        return self

    def set_order_type(self, order_type: str):
        self.request.orderType = order_type
        return self

    def set_side(self, side: str):
        self.request.side = side
        return self

    def set_qty(self, qty: str):
        self.request.qty = qty
        return self

    def set_start_time(self, start_time: int):
        self.request.startTime = start_time
        return self

    def set_end_time(self, end_time: int):
        self.request.endTime = end_time
        return self

    def build(self):
        """
        Finalize and return the configured RequestParameters object.
        """
        return self.request


# builder = BrokerRequestBuilder()
# request = (
#     builder.set_broker("SomeBroker")
#            .set_position_idx(1)
#            .set_base_coin("BTC")
#            .set_settle_coin("USD")
#            .set_buy_leverage("10x")
#            .set_sell_leverage("5x")
#            .build()
# )
#
# print(request)
