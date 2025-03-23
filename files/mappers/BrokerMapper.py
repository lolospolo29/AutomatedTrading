
from files.models.broker.BrokerOrder import BrokerOrder
from files.models.broker.BrokerPosition import BrokerPosition
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade


class BrokerMapper:

    @staticmethod
    def map_broker_order_to_order(broker_order:BrokerOrder, order:Order, check_time:bool=False) -> Order:
            try:
                if order.updated_time > broker_order.updatedTime and check_time:
                        return order
            except Exception as e:
                order.order_type = broker_order.orderType
                order.order_link_id = broker_order.orderLinkId
                order.symbol = broker_order.symbol
                order.category = broker_order.category
                order.qty = broker_order.qty
                order.order_id = broker_order.orderId
                order.is_leverage = broker_order.isLeverage
                order.market_unit = broker_order.marketUnit
                order.order_iv = broker_order.orderIv
                order.stop_loss = broker_order.stopLoss
                order.take_profit = broker_order.takeProfit
                order.price = broker_order.price
                order.time_in_force = broker_order.timeInForce
                order.close_on_trigger = broker_order.closeOnTrigger
                order.reduce_only = broker_order.reduceOnly
                order.trigger_price = broker_order.triggerPrice
                order.trigger_by = broker_order.triggerBy
                order.tp_trigger_by = broker_order.tpTriggerBy
                order.sl_trigger_by = broker_order.slTriggerBy
                order.trigger_direction = broker_order.triggerDirection
                order.tpsl_mode = broker_order.tpslMode
                order.tp_limit_price = broker_order.tpLimitPrice
                order.sl_limit_price = broker_order.slLimitPrice
                order.created_time = broker_order.createdTime
                order.updated_time = broker_order.updatedTime
                order.last_price_on_created = broker_order.lastPriceOnCreated
                order.leaves_qty = broker_order.leavesQty
                order.stop_order_type = broker_order.stopOrderType
                order.order_status = broker_order.orderStatus
                order.leaves_value = broker_order.leavesValue
                return order

    @staticmethod
    def map_broker_position_to_trade(broker_position:BrokerPosition, trade:Trade, check_time:bool=True) -> Trade:
            try:
                if int(broker_position.updatedTime) < int(trade.updated_time) and check_time:
                    return trade
            except Exception:
                pass
            if trade.updated_time is None and broker_position.updatedTime is not None:
                trade.created_time = broker_position.createdTIme
                trade.updated_time = broker_position.updatedTime
                trade.trade_mode = broker_position.tradeMode
                trade.side = broker_position.side
                trade.tpsl_mode = broker_position.tpslMode
                trade.unrealised_pnl = broker_position.unrealisedPnl
                trade.leverage = broker_position.leverage
                trade.size = broker_position.size
                trade.trade_mode = broker_position.tradeMode
