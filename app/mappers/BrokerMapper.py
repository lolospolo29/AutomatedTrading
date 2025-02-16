
from app.api.brokers.models.BrokerOrder import BrokerOrder
from app.api.brokers.models.BrokerPosition import BrokerPosition
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class BrokerMapper:

    # noinspection PyArgumentList
    @staticmethod
    def map_broker_order_to_order(broker_order:BrokerOrder, order:Order,check_time:bool=False) -> Order:
        try:
            try:
                if order.updatedTime > broker_order.updatedTime and check_time:
                        return order
            except Exception as e:
                logger.error(f"Mapping Error for Order,OrderLinkId: {order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol},Error: {e}")
                order.orderType = broker_order.orderType
                order.orderLinkId = broker_order.orderLinkId
                order.symbol = broker_order.symbol
                order.category = broker_order.category
                order.qty = broker_order.qty
                order.orderId = broker_order.orderId
                order.isLeverage = broker_order.isLeverage
                order.marketUnit = broker_order.marketUnit
                order.orderIv = broker_order.orderIv
                order.stopLoss = broker_order.stopLoss
                order.takeProfit = broker_order.takeProfit
                order.price = broker_order.price
                order.timeInForce = broker_order.timeInForce
                order.closeOnTrigger = broker_order.closeOnTrigger
                order.reduceOnly = broker_order.reduceOnly
                order.triggerPrice = broker_order.triggerPrice
                order.triggerBy = broker_order.triggerBy
                order.tpTriggerBy = broker_order.tpTriggerBy
                order.slTriggerBy = broker_order.slTriggerBy
                order.triggerDirection = broker_order.triggerDirection
                order.tpslMode = broker_order.tpslMode
                order.tpLimitPrice = broker_order.tpLimitPrice
                order.slLimitPrice = broker_order.slLimitPrice
                order.createdTime = broker_order.createdTime
                order.updatedTime = broker_order.updatedTime
                order.lastPriceOnCreated = broker_order.lastPriceOnCreated
                order.leavesQty = broker_order.leavesQty
                order.stopOrderType = broker_order.stopOrderType
                order.orderStatus = broker_order.orderStatus
                order.leavesValue = broker_order.leavesValue
                return order
        except Exception as e:
            logger.error(f"Mapping Error for Order,OrderLinkId: {order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol},Error: {e}")

    @staticmethod
    def map_broker_position_to_trade(broker_position:BrokerPosition, trade:Trade,check_time:bool=True) -> Trade:
        try:
            try:
                if int(broker_position.updatedTime) < int(trade.updatedTime) and check_time:
                    return trade
            except Exception:
                logger.debug(broker_position.updatedTime,trade.updatedTime)
            if trade.updatedTime is None and broker_position.updatedTime is not None:
                trade.createdTime = broker_position.createdTIme
                trade.updatedTime = broker_position.updatedTime
                trade.tradeMode = broker_position.tradeMode
                trade.side = broker_position.side
                trade.tpslMode = broker_position.tpslMode
                trade.unrealisedPnl = broker_position.unrealisedPnl
                trade.leverage = broker_position.leverage
                trade.size = broker_position.size
                trade.tradeMode = broker_position.tradeMode
                trade.positionValue = broker_position.positionValue

        except Exception as e:
            logger.error(f"Update Trade Error,TradeId: {trade.id}: {e}")
        finally:
            return trade
