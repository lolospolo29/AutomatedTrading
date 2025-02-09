from dataclasses import fields

from app.api.brokers.models.BrokerOrder import BrokerOrder
from app.api.brokers.models.BrokerPosition import BrokerPosition
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class BrokerMapper:

    @staticmethod
    def map_broker_order_to_order(broker_order:BrokerOrder, order:Order,check_time:bool=False) -> Order:
        try:
            try:
                if order.updatedTime > broker_order.updatedTime and check_time:
                        return order
            finally:
                broker_fields = {field.name for field in fields(BrokerOrder)}

                # Get attribute names of Order (excluding methods and special attributes)
                order_fields = {attr for attr in dir(order) if
                                not callable(getattr(order, attr)) and not attr.startswith("__")}

                # Find common fields
                common_fields = broker_fields.intersection(order_fields)

                for field_name in common_fields:
                    value = getattr(broker_order, field_name, None)
                    if value is not None:  # Only set if value is not None
                        setattr(order, field_name, value)

                return order

        except Exception as e:
            logger.error(f"Mapping Error for Order,OrderLinkId: {order.orderLinkId},TradeId:{order.trade_id},Symbol:{order.symbol},Error: {e}")

    @staticmethod
    def map_broker_position_to_trade(broker_position:BrokerPosition, trade:Trade,check_time:bool=True) -> Trade:
        try:
            if int(broker_position.updatedTime) > int(trade.updatedTime) and check_time:
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

                return trade
        except Exception as e:
            logger.error(f"Update Trade Error,TradeId: {trade.id}: {e}")
        finally:
            return trade
