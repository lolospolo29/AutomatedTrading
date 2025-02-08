from datetime import datetime
from typing import Optional, Dict, Any

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.frameworks.Structure import Structure
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade
from app.monitoring.logging.logging_startup import logger


class TradeMapper:
    """Maps from the Trade/Order Modells"""

    @staticmethod
    def parse_datetime(field: Any) -> Optional[datetime]:
        """
        Parse MongoDB datetime fields.
        Returns None if the field is not a valid datetime or is missing.
        """
        try:
            if isinstance(field, dict) and "$date" in field:
                    return datetime.fromisoformat(field["$date"].replace("Z", ""))
            return field
        except Exception:
            raise ValueError("Invalid datetime field")

    def map_candle(self,candle_data: Dict[str, Any]) -> Optional[Candle]:
        """
        Map Candle data, returning None if required fields are missing.
        """
        try:
            return Candle(
                asset=candle_data.get("asset"),
                broker=candle_data.get("broker"),
                open=candle_data.get("open"),
                high=candle_data.get("high"),
                low=candle_data.get("low"),
                close=candle_data.get("close"),
                iso_time=self.parse_datetime(candle_data.get("iso_time")),
                timeframe=int(candle_data.get("timeframe")),
                id=candle_data.get("id")
            )
        except Exception as e:
            logger.error(f"Mapping Candle Error: {e}")

    def map_framework(self,data: Dict[str, Any]) -> Optional[Any]:
        """
        Map framework data dynamically based on type.
        Returns None if the type is unrecognized or fields are missing.
        """
        try:
            if "PDArray" in data:
                pd_array = data.get("PDArray", {})
                framework = PDArray(pd_array.get("name", ""), pd_array.get("direction", ""))
                candles = [self.map_candle(c) for c in pd_array.get("candles", []) if c]
                framework.add_candles(candles)
                framework.timeFrame = pd_array.get("timeframe", "")
                return framework

            if "Level" in data:
                level = data.get("Level", {})
                candles = [self.map_candle(c) for c in level.get("candles", []) if c]
                framework = Level(level.get("name", ""), level.get("level"))
                framework.set_fib_level(level.get("fib_level", 0.0), level.get("direction", ""), candles)
                return framework

            if "Structure" in data:
                structure = data.get("Structure", {})
                candle = structure.get("candles", {}).get("Candle")
                framework = Structure(structure.get("name", ""), structure.get("direction", ""), candle=candle)
                return framework
            return None
        except Exception:
            raise ValueError("Invalid framework data")

    def map_order_from_db(self,order_data: Dict[str, Any]) -> Optional[Order]:
        """
        Map Order data from MongoDB document.
        Returns None if required fields are missing.
        """
        try:
            order_dict = order_data.get("Order", {})
            order = Order()

            # List of attributes to set dynamically
            attributes = [
                "trade_id", "orderStatus", "risk_percentage", "order_result_status","money_at_risk", "unrealisedPnL",
                "orderLinkId", "orderType", "symbol", "category", "side", "qty", "orderId",
                "isLeverage", "marketUnit", "orderFilter", "orderIv", "stopLoss", "takeProfit",
                "price", "timeInForce", "closeOnTrigger", "reduceOnly", "triggerPrice",
                "triggerBy", "tpTriggerBy", "slTriggerBy", "triggerDirection", "tpslMode",
                "tpLimitPrice", "tpOrderType", "slOrderType", "slLimitPrice", "lastPriceOnCreated","createdTime",
                "updatedTime","leavesQty","stopOrderType","orderStatus","leavesValue"
            ]

            # Dynamically assign attributes
            for attr in attributes:
                setattr(order, attr, order_dict.get(attr))
            # Parse datetime fields
            # Map frameworks
            logger.info(f"Mapping Order,OrderLinkId:{order_dict.get('orderLinkId')},Symbol:{order.symbol},TradeId:{order.trade_id}")
            try:
                order.entry_frame_work = self.map_framework(order_dict.get("entry_frame_work", {}))
            except Exception:
                pass
            order.confirmations = [
                self.map_framework(cf) for cf in order_dict.get("confirmations", []) if cf
            ]

            return order
        except Exception:
            raise ValueError("Invalid Order data")

    @staticmethod
    def map_trade_from_db(trade_data: Dict[str, Any]) -> Optional[Trade]:
        """
        Map Trade data from MongoDB document.
        Returns None if required fields are missing.
        """
        try:
            logger.debug("Mapping Trade,TradeId:{trade_id}".format(trade_id=trade_data.get("trade_id")))
            relation = AssetBrokerStrategyRelation(
                asset=trade_data.get("asset", ""),
                broker=trade_data.get("broker", ""),
                strategy=trade_data.get("strategy", ""),
                max_trades=1
            )
            trade = Trade(
                relation=relation,
                id=trade_data.get("id")
            )

            logger.info(f"Mapping Trade,TradingId:{trade.id}")
            # Set additional attributes
            trade.category = trade_data.get("category", "")
            trade.side = trade_data.get("side", "")
            trade.tpslMode = trade_data.get("tpslMode", "")
            trade.unrealisedPnl = trade_data.get("unrealisedPnl")
            trade.leverage = trade_data.get("leverage")
            trade.size = trade_data.get("size")
            trade.tradeMode = trade_data.get("tradeMode")
            trade.updatedTime = trade_data.get("updatedTime")
            trade.createdTime = trade_data.get("createdTime")
            trade.positionValue = trade_data.get("positionValue")

            return trade
        except Exception:
            raise ValueError("Invalid Trade data")

# todo refactor mapping