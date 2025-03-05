import uuid
from typing import Optional

from pydantic import Field

from app.helper.builder.OrderBuilder import OrderBuilder
from app.models.frameworks.pdarray.PDEnum import PDEnum
from app.models.frameworks.structure.StructureEnum import StructureEnum
from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Candle import Candle
from app.models.asset.Relation import Relation
from app.models.frameworks.FrameWork import FrameWork
from app.models.frameworks.Level import Level
from app.models.frameworks.PDArray import PDArray
from app.models.frameworks.Structure import Structure
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
        if timeFrame == 1 and len(candles) >= 240:
            bosS = self.strategy_facade.StructureMediator.calculate_confirmation(StructureEnum.BREAKOFSTRUCTURE.value, candles= candles)

            for bos in bosS:
                self.strategy_facade.structure_handler.add_structure(bos)

            pds = []

            pds.extend(self.strategy_facade.PDMediator.calculate_pd_array(pd_type=PDEnum.BPR.value, candles= candles))
            pds.extend(self.strategy_facade.PDMediator.calculate_pd_array(pd_type=PDEnum.BREAKER.value, candles= candles))
            pds.extend(self.strategy_facade.PDMediator.calculate_pd_array_with_lookback(pd_type=PDEnum.FVG.value, candles= candles,lookback=3))
            pds.extend(self.strategy_facade.PDMediator.calculate_pd_array_with_lookback(pd_type=PDEnum.OrderBlock.value, candles= candles,lookback=2))

            for pd in pds:
                self.strategy_facade.pd_array_handler.add_pd_array(pd)

            self.strategy_facade.pd_array_handler.remove_pd_array(candles, timeFrame)
            self.strategy_facade.structure_handler.remove_structure(candles, timeFrame)

    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str) ->StrategyResult:

        self._analyzeData(candles, timeFrame)

        structures:list[Structure] = self.strategy_facade.structure_handler.return_structure()
        pds:list[PDArray] = self.strategy_facade.pd_array_handler.detect_swing()

        levels:list[Level] = []
        levels.extend(self.strategy_facade.LevelMediator.calculate_fibonacci(level_type=LevelEnum.OPTIMALTRADEENTRY.value,
                                                                           candles=candles, lookback=240))
        levels.extend(self.strategy_facade.LevelMediator.calculate_fibonacci(level_type=LevelEnum.PREMIUMDISCOUNT.value,
                                                                           candles=candles, lookback=240))

        if candles and levels and pds and structures and timeFrame == 1:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            if not self.is_in_time(time):
                return StrategyResult()

            last_structure:FrameWork = structures[-1]

            levels = levels[-9:]

            fib_high = None
            fib_low = None
            fib_eq = None
            bullish_low_ote = None
            bearish_high_ote = None

            profit_stop_entry = []

            for level in levels:
                if level.fib_level == 0.79 and level.direction == "Bullish":
                    bullish_low_ote = level.level
                if level.fib_level == 0.0 and level.direction == "Bullish":
                    fib_low = level.level
                if level.fib_level == 0.5 and level.direction == "EQ":
                    fib_eq = level.level
                if level.fib_level == 0.79 and level.direction == "Bearish":
                    bearish_high_ote = level.level
                if level.fib_level == 1.0 and level.direction == "Bearish":
                    fib_high = level.level
                profit_stop_entry.extend([candle.close for candle in level._candles])

            if last_structure.direction == "Bullish" and last_candle.close > fib_eq or last_candle.low < fib_low:
                return StrategyResult()
            if last_structure.direction == "Bearish" and last_candle.close < fib_eq or last_candle.high > fib_high:
                return StrategyResult()

            entry = []

            for pd in pds:
                pd: PDArray = pd
                if pd.name == PDEnum.FVG.value or pd.name == PDEnum.OrderBlock.value or pd.name == PDEnum.BREAKER.value or pd.name == PDEnum.BPR.value:
                    for candle in pd.candles:
                        if last_structure.direction == "Bullish":
                            if candle.close <= fib_eq:
                                entry.append(candle.close)
                        if last_structure.direction == "Bearish":
                            if candle.close >= fib_eq:
                                entry.append(candle.close)

            high = max(entry)
            low = min(entry)

            stop = None
            take_profit = None
            order_dir = None
            exit_dir = None
            profit_dir = None
            stop_dir = None

            if low < last_candle.close <= high and last_structure.direction == "Bullish" and last_candle.close > bullish_low_ote:
                stop = fib_low
                take_profit = bearish_high_ote
                order_dir = OrderDirectionEnum.BUY.value
                exit_dir = OrderDirectionEnum.SELL.value
                profit_dir = TriggerDirection.RISE.value
                stop_dir = TriggerDirection.FALL.value

            if low <= last_candle.close < high and last_structure.direction == "Bearish" and last_candle.close < bearish_high_ote:
                stop = fib_high
                take_profit = bullish_low_ote
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
