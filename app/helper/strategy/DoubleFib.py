import uuid
from typing import Optional

from pydantic import Field

from app.helper.builder.OrderBuilder import OrderBuilder
from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Candle import Candle
from app.models.asset.Relation import Relation
from app.models.frameworks.Level import Level
from app.models.strategy.Strategy import Strategy
from app.models.trade.Trade import Trade
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.enums.CategoryEnum import CategoryEnum
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.models.trade.enums.TriggerByEnum import TriggerByEnum
from app.models.trade.enums.TriggerDirectionEnum import TriggerDirection
from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum


# Double Fib

class DoubleFib(Strategy):
    model_config = {
        "arbitrary_types_allowed": True
    }

    strategy_facade: Optional['StrategyFacade'] = Field(default=None)

    def _analyzeData(self, candles: list[Candle], timeFrame: int):
        if timeFrame == 1 and len(candles) > 60:
            ote = self.strategy_facade.LevelMediator.calculate_fibonacci(level_type="OTE", candles= candles, lookback=60)
            for level in ote:
                self.strategy_facade.level_handler.add_level(level)
            self.strategy_facade.level_handler.remove_level(candles, timeFrame)

    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str) ->StrategyResult:

        self._analyzeData(candles, timeFrame)
        levels:list[Level] = self.strategy_facade.level_handler.return_levels()
        if candles and levels and timeFrame == 1:


            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            if not self.is_in_time(time):
                return StrategyResult()

            levels:list[Level] = levels[-6:]

            bullish_ote_level_min = None
            bullish_ote_level_max = None
            bearish_ote_level_min = None
            bearish_ote_level_max = None

            profit_stop_entry = []

            for level in levels:
                if level.fib_level == 0.75 and level.direction == "Bullish":
                    bullish_ote_level_min = level.level
                if level.fib_level == 0.62 and level.direction == "Bullish":
                    bullish_ote_level_max = level.level
                if level.fib_level == 0.75 and level.direction == "Bearish":
                    bearish_ote_level_max = level.level
                if level.fib_level == 0.62 and level.direction == "Bearish":
                    bearish_ote_level_min = level.level
                profit_stop_entry.extend([candle.close for candle in level.candles])

            stop = None
            take_profit = None
            order_dir = None
            exit_dir = None
            profit_dir = None
            stop_dir = None

            if bullish_ote_level_min <= last_candle.close <= bullish_ote_level_max:
                stop = min(profit_stop_entry)
                take_profit = max(profit_stop_entry)
                order_dir = OrderDirectionEnum.BUY.value
                exit_dir = OrderDirectionEnum.SELL.value
                profit_dir = TriggerDirection.RISE.value
                stop_dir = TriggerDirection.FALL.value

            if bearish_ote_level_min <= last_candle.close <= bearish_ote_level_max:
                stop = max(profit_stop_entry)
                take_profit = min(profit_stop_entry)
                order_dir = OrderDirectionEnum.SELL.value
                exit_dir = OrderDirectionEnum.BUY.value
                profit_dir = TriggerDirection.FALL.value
                stop_dir = TriggerDirection.RISE.value

            if order_dir:
                trade = Trade(relation=relation,category=CategoryEnum.LINEAR.value,orders=[],tradeId=str(uuid.uuid4()))
                trade.side = order_dir

                entry_order = OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                    ,category=CategoryEnum.LINEAR.value, side=order_dir
                                                    ,risk_percentage=1
                                                    ,order_number=1
                                                    ,tradeId=trade.tradeId).build()

                stop_order =  OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                          ,category=CategoryEnum.LINEAR.value, side=exit_dir
                                                          ,risk_percentage=1
                                                          ,order_number=2
                                                          ,tradeId=trade.tradeId).set_conditional(
                                                          trigger_direction=stop_dir
                                                          ,trigger_price=stop,trigger_by=
                                                          TriggerByEnum.MARKPRICE.value).set_defaults(price=stop).build()

                take_profit_order =  OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                          ,category=CategoryEnum.LINEAR.value, side=exit_dir
                                                          ,risk_percentage=1
                                                          ,order_number=3
                                                          ,tradeId=trade.tradeId).set_conditional(
                                                          trigger_direction=profit_dir
                                                          ,trigger_price=take_profit,trigger_by=
                                                          TriggerByEnum.MARKPRICE.value).set_defaults(price=take_profit).build()

                qty = str(self.strategy_facade.risk_calculator.calculate_order_qty(asset_class=asset_class
                                                                                    , entry_price=float(last_candle.close)
                                                                                    , exit_price=float(stop_order.price)))

                entry_order.qty = qty
                take_profit_order.qty = qty
                stop_order.qty = qty

                trade.orders.append(entry_order)
                trade.orders.append(stop_order)
                trade.orders.append(take_profit_order)

                return StrategyResult(trade=trade,status=StrategyResultStatusEnum.NEWTRADE.value)
            else:
                return StrategyResult()
        else:
            return StrategyResult()

    def get_exit(self, candles: list, timeFrame: int, trade:Trade, relation:Relation)->StrategyResult:

        # todo trail stop
        return StrategyResult(trade=trade,status=StrategyResultStatusEnum.NOCHANGE.value)
