from datetime import datetime

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.frameworks.Structure import Structure
from app.models.trade.Order import Order
from app.models.trade.Trade import Trade


class TradeMapper:

    @staticmethod
    def mapTradeFromDB(trade:dict) -> Trade:
        trade = trade.get('Trade')
        id = trade.get("id")
        asset = trade.get("asset")
        broker = trade.get("broker")
        strategy = trade.get("strategy")
        orders = trade.get("orders")
        relation = AssetBrokerStrategyRelation(asset=asset,broker=broker,strategy=strategy,maxTrades=1)

        mappedTrade = Trade(relation=relation,orders=orders)
        mappedTrade.id = id
        return mappedTrade

    @staticmethod
    def parse_datetime(field):
        """Parse MongoDB datetime fields."""
        if isinstance(field, dict) and "$date" in field:
            return datetime.fromisoformat(field["$date"].replace("Z", ""))
        return field

    def map_candle(self,candle_data):
        """Map Candle data."""
        return Candle(
            asset=candle_data["Candle"]["asset"],
            broker=candle_data["Candle"]["broker"],
            open=candle_data["Candle"]["open"],
            high=candle_data["Candle"]["high"],
            low=candle_data["Candle"]["low"],
            close=candle_data["Candle"]["close"],
            IsoTime=self.parse_datetime(candle_data["Candle"]["IsoTime"]),
            timeFrame=candle_data["Candle"]["timeFrame"],
            id=candle_data["Candle"]["id"]
        )

    def map_framework(self,data):
        """Map framework data dynamically based on type."""
        if "PDArray" in data:
            pd_array = data["PDArray"]
            framework = PDArray(pd_array["name"], pd_array["direction"])
            for candle in pd_array.get("candles", []):
                framework.addCandles([self.map_candle(candle)])
            return framework
        elif "Level" in data:
            level = data["Level"]
            candles = []
            for candle in level.get("candles", []):
                candles.append(self.map_candle(candle))
            framework = Level(level["name"], level["level"])
            framework.setFibLevel(level.get("fibLevel", 0.0), level["direction"],candles=candles)
            return framework
        elif "Structure" in data:
            structure = data["Structure"]
            candles = []
            candle = structure.get("candles").get("Candle")
            return Structure(structure["name"], structure["direction"],candle=candle)
        return None

    def mapOrderFromDB(self,mongo_data: dict):
        """Map Order data from MongoDB document."""
        order_dict = mongo_data["Order"]
        order = Order()

        order.tradeId = order_dict.get("tradeId")
        order.status = order_dict.get("status")
        order.entryFrameWork = self.map_framework(order_dict["entryFrameWork"])
        order.confirmations = [self.map_framework(cf) for cf in order_dict["confirmations"]]
        order.createdAt = self.parse_datetime(order_dict["createdAt"])
        order.openedAt = self.parse_datetime(order_dict.get("openedAt"))
        order.closedAt = self.parse_datetime(order_dict.get("closedAt"))
        order.updatedAt = self.parse_datetime(order_dict["updatedAt"])
        order.riskPercentage = order_dict.get("riskPercentage")
        order.moneyAtRisk = order_dict.get("moneyAtRisk")
        order.unrealisedPnL = order_dict.get("unrealisedPnL")
        order.orderLinkId = order_dict.get("orderLinkId")
        order.orderType = order_dict.get("orderType")
        order.symbol = order_dict.get("symbol")
        order.category = order_dict.get("category")
        order.side = order_dict.get("side")
        order.qty = order_dict.get("qty")
        order.orderId = order_dict.get("orderId")
        order.isLeverage = order_dict.get("isLeverage")
        order.marketUnit = order_dict.get("marketUnit")
        order.orderFilter = order_dict.get("orderFilter")
        order.orderlv = order_dict.get("orderlv")
        order.stopLoss = order_dict.get("stopLoss")
        order.takeProfit = order_dict.get("takeProfit")
        order.price = order_dict.get("price")
        order.timeInForce = order_dict.get("timeInForce")
        order.closeOnTrigger = order_dict.get("closeOnTrigger")
        order.reduceOnly = order_dict.get("reduceOnly")
        order.triggerPrice = order_dict.get("triggerPrice")
        order.triggerBy = order_dict.get("triggerBy")
        order.tpTriggerBy = order_dict.get("tpTriggerBy")
        order.slTriggerBy = order_dict.get("slTriggerBy")
        order.triggerDirection = order_dict.get("triggerDirection")
        order.tpslMode = order_dict.get("tpslMode")
        order.tpLimitPrice = order_dict.get("tpLimitPrice")
        order.tpOrderType = order_dict.get("tpOrderType")
        order.slOrderType = order_dict.get("slOrderType")
        order.slLimitPrice = order_dict.get("slLimitPrice")

        return order
