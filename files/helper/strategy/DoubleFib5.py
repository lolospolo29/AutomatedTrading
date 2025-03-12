import uuid

from files.helper.builder.OrderBuilder import OrderBuilder
from files.helper.calculator.RiskCalculator import RiskCalculator
from files.helper.mediator.PriceMediator import PriceMediator
from files.interfaces.ITimeWindow import ITimeWindow
from files.models.asset.Candle import Candle
from files.models.asset.Relation import Relation
from files.models.frameworks.FrameWork import FrameWork
from files.models.frameworks.time.London import LondonOpen
from files.models.frameworks.time.NYOpen import NYOpen
from files.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from files.models.strategy.Strategy import Strategy
from files.models.strategy.StrategyResult import StrategyResult
from files.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from files.models.trade.Trade import Trade
from files.models.trade.enums.CategoryEnum import CategoryEnum
from files.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from files.models.trade.enums.TriggerByEnum import TriggerByEnum
from files.models.trade.enums.TriggerDirectionEnum import TriggerDirection


# Double Fib

class DoubleFib5(Strategy):

    def __init__(self,):
        self.name = "DoubleFib5"
        self.timeframes = []

        self.timeframes.append(ExpectedTimeFrame(timeframe=5,max_Len=90))

        self._timewindow:ITimeWindow = NYOpen()
        self._timewindow3:ITimeWindow = LondonOpen()
        self.time_windows = [self._timewindow,self._timewindow3]
        self._price_mediator:PriceMediator = PriceMediator()
        self._risk_calculator:RiskCalculator = RiskCalculator()

    def is_in_time(self, time) -> bool:
        for timewindow in self.time_windows:
            timewindow:ITimeWindow = timewindow
            if timewindow.is_in_entry_window(time):
                return True
        return False

    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str) ->StrategyResult:

        if len(candles) >= 3:
            self._price_mediator.detect_pd_arrays(first_candle=candles[-3],second_candle=candles[-2],third_candle=candles[-1]
                                                  ,timeframe=timeFrame)
        else:
            return StrategyResult()

        if candles and timeFrame == 5:

            third_candle: Candle = candles[-1]
            second_candle: Candle = candles[-2]
            first_candle: Candle = candles[-3]

            time = third_candle.iso_time

            bos = self._price_mediator.get_bos(timeFrame)

            imbalances = self._price_mediator.get_imbalances(timeFrame)

            if len(imbalances) > 900 or third_candle.iso_time.year != second_candle.iso_time.year:
                self._price_mediator.reset()

            if not bos or not imbalances:
                return StrategyResult()

            levels = self._price_mediator.get_fibonnaci(bos.candles,ote=True)

            levels.extend(self._price_mediator.get_fibonnaci(bos.candles,pd=True))

            fib_levels,profit_stop_entry = self._get_fibonacci_levels(levels)

            if bos.direction == "Bullish" and (third_candle.close > fib_levels["fib_eq"] or third_candle.low < fib_levels["fib_low"]):
                return StrategyResult()
            if bos.direction == "Bearish" and (third_candle.close < fib_levels["fib_eq"] or third_candle.high > fib_levels["fib_high"]):
                return StrategyResult()

            stop = None
            take_profit = None
            order_dir = None
            exit_dir = None
            profit_dir = None
            stop_dir = None

            if fib_levels["fib_low"] < third_candle.close < fib_levels["fib_high"]:
                if bos.direction == "Bullish" and fib_levels["bullish_low_ote"] < third_candle.close < fib_levels["bullish_high_ote"]:
                    stop = fib_levels["fib_low"]
                    take_profit = fib_levels["fib_high"]
                    order_dir = OrderDirectionEnum.BUY.value
                    exit_dir = OrderDirectionEnum.SELL.value
                    profit_dir = TriggerDirection.RISE.value
                    stop_dir = TriggerDirection.FALL.value
                if bos.direction == "Bearish" and fib_levels["bearish_low_ote"] < third_candle.close < fib_levels["bearish_high_ote"]:
                    stop = fib_levels["fib_high"]
                    take_profit = fib_levels["fib_low"]
                    order_dir = OrderDirectionEnum.SELL.value
                    exit_dir = OrderDirectionEnum.BUY.value
                    profit_dir = TriggerDirection.FALL.value
                    stop_dir = TriggerDirection.RISE.value

            # if not self.is_in_time(time):
            #      return StrategyResult()

            if order_dir:

                trade = self._create_trade(relation=relation,order_dir=order_dir
                                           ,exit_dir=exit_dir,profit_dir=profit_dir
                                           ,stop_dir=stop_dir,take_profit=take_profit
                                           ,stop=stop,last_candle=third_candle
                                           ,asset_class=asset_class,levels=levels)

                return StrategyResult(trade=trade,status=StrategyResultStatusEnum.NEWTRADE.value)
            else:
                return StrategyResult()
        else:
            return StrategyResult()

    def get_exit(self, candles: list, timeFrame: int, trade:Trade, relation:Relation)->StrategyResult:

        return StrategyResult(trade=trade,status=StrategyResultStatusEnum.NOCHANGE.value)

    def _create_trade(self,relation:Relation,order_dir:str,exit_dir:str,stop_dir:str
                      ,profit_dir:str,take_profit:float,stop:float,last_candle:Candle,asset_class:str,levels:list[FrameWork]):
        trade = Trade(relation=relation, category=CategoryEnum.LINEAR.value, orders=[], tradeId=str(uuid.uuid4()))
        trade.side = order_dir

        entry_order = OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                  , category=CategoryEnum.LINEAR.value, side=order_dir
                                                  , risk_percentage=1
                                                  , order_number=1,
                                                  tradeId=trade.tradeId).build()

        stop_order = OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                 , category=CategoryEnum.LINEAR.value, side=exit_dir
                                                 , risk_percentage=1
                                                 , order_number=2
                                                 , tradeId=trade.tradeId).set_conditional(
            trigger_direction=stop_dir
            , trigger_price=stop, trigger_by=
            TriggerByEnum.MARKPRICE.value).set_defaults(price=stop).build()

        take_profit_order = OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                        , category=CategoryEnum.LINEAR.value, side=exit_dir
                                                        , risk_percentage=1
                                                        , order_number=3
                                                        , tradeId=trade.tradeId).set_conditional(
            trigger_direction=profit_dir
            , trigger_price=take_profit, trigger_by=
            TriggerByEnum.MARKPRICE.value).set_defaults(price=take_profit).build()

        qty = str(self._risk_calculator.calculate_order_qty(asset_class=asset_class
                                                            , entry_price=float(last_candle.close)
                                                            , exit_price=float(stop_order.price)))

        entry_order.qty = qty
        take_profit_order.qty = qty
        stop_order.qty = qty

        trade.orders.append(entry_order)
        trade.orders.append(stop_order)
        trade.orders.append(take_profit_order)

        return trade

    @staticmethod
    def _get_fibonacci_levels(levels)->tuple[dict,list]:
        fib_levels = {
            "fib_high": None,
            "fib_low": None,
            "fib_eq": None,
            "fib_bearish_tp": None,
            "fib_bullish_tp": None,
            "bullish_low_ote": None,
            "bearish_high_ote": None
        }

        profit_stop_entry = []

        for level in levels:
            if level.fib_level == 0.705 and level.direction == "Bullish":
                fib_levels["bullish_low_ote"] = level.level
            if level.fib_level == 0.62 and level.direction == "Bullish":
                fib_levels["bullish_high_ote"] = level.level
            if level.fib_level == 0.705 and level.direction == "Bearish":
                fib_levels["bearish_high_ote"] = level.level
            if level.fib_level == 0.62 and level.direction == "Bearish":
                fib_levels["bearish_low_ote"] = level.level
            if level.fib_level == 1.0 and level.direction == "Bullish":
                fib_levels["fib_low"] = level.level
            if level.fib_level == 0.5:
                fib_levels["fib_eq"] = level.level
            if level.fib_level == 0.0 and level.direction == "Bullish":
                fib_levels["fib_high"] = level.level
            if level.fib_level == 1.5 and level.direction == "Bullish":
                fib_levels["fib_bullish_tp"] = level.level
            if level.fib_level == 1.5 and level.direction == "Bearish":
                fib_levels["fib_bearish_tp"] = level.level

            profit_stop_entry.extend([candle.close for candle in level.candles])

        return fib_levels, profit_stop_entry

