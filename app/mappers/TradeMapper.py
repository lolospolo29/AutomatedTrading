from typing import Optional, Dict, Any, List
from datetime import datetime

from app.mappers.exceptions.MappingFailedExceptionError import MappingFailedExceptionError
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.frameworks.Structure import Structure
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade


class TradeMapper:
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
            raise MappingFailedExceptionError("Datetime")

    def map_candle(self,candle_data: Dict[str, Any]) -> Optional[Candle]:
        """
        Map Candle data, returning None if required fields are missing.
        """
        try:
            candle = candle_data.get("Candle", {})
            return Candle(
                asset=candle.get("asset"),
                broker=candle.get("broker"),
                open=candle.get("open", 0.0),
                high=candle.get("high", 0.0),
                low=candle.get("low", 0.0),
                close=candle.get("close", 0.0),
                iso_time=self.parse_datetime(candle.get("iso_time")),
                timeframe=candle.get("timeframe", ""),
                id=candle.get("id")
            )
        except Exception:
            raise MappingFailedExceptionError("Candle")

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
                framework.timeFrame = pd_array.get("timeFrame", "")
                return framework

            if "Level" in data:
                level = data.get("Level", {})
                candles = [self.map_candle(c) for c in level.get("candles", []) if c]
                framework = Level(level.get("name", ""), level.get("level", 0.0))
                framework.set_fib_level(level.get("fib_level", 0.0), level.get("direction", ""), candles)
                return framework

            if "Structure" in data:
                structure = data.get("Structure", {})
                candle = structure.get("candles", {}).get("Candle")
                framework = Structure(structure.get("name", ""), structure.get("direction", ""), candle=candle)
                return framework
            return None
        except Exception:
            raise MappingFailedExceptionError("Framework")

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
                "trade_id", "orderStatus", "risk_percentage", "money_at_risk", "unrealisedPnL",
                "orderLinkId", "orderType", "symbol", "category", "side", "qty", "orderId",
                "isLeverage", "marketUnit", "orderFilter", "orderlv", "stopLoss", "takeProfit",
                "price", "timeInForce", "closeOnTrigger", "reduceOnly", "triggerPrice",
                "triggerBy", "tpTriggerBy", "slTriggerBy", "triggerDirection", "tpslMode",
                "tpLimitPrice", "tpOrderType", "slOrderType", "slLimitPrice", "lastPriceOnCreated"
            ]

            # Dynamically assign attributes
            for attr in attributes:
                setattr(order, attr, order_dict.get(attr))

            # Parse datetime fields

            # Map frameworks
            order.entry_frame_work = self.map_framework(order_dict.get("entry_frame_work", {}))
            order.confirmations = [
                self.map_framework(cf) for cf in order_dict.get("confirmations", []) if cf
            ]

            return order
        except Exception:
            raise MappingFailedExceptionError("Order")

    @staticmethod
    def map_trade_from_db(trade_data: Dict[str, Any]) -> Optional[Trade]:
        """
        Map Trade data from MongoDB document.
        Returns None if required fields are missing.
        """
        try:
            trade_dict = trade_data.get("Trade", {})
            relation = AssetBrokerStrategyRelation(
                asset=trade_dict.get("asset", ""),
                broker=trade_dict.get("broker", ""),
                strategy=trade_dict.get("strategy", ""),
                max_trades=1
            )

            trade = Trade(
                relation=relation,
                orders=trade_dict.get("orders", []),
                id=trade_dict.get("id")
            )

            # Set additional attributes
            trade.side = trade_dict.get("side", "")
            trade.size = trade_dict.get("size", 0.0)
            trade.tradeMode = trade_dict.get("tradeMode", "")
            trade.unrealisedPnl = trade_dict.get("unrealisedPnl", 0.0)
            trade.leverage = trade_dict.get("leverage", 0.0)

            return trade
        except Exception:
            raise MappingFailedExceptionError("Trade")
