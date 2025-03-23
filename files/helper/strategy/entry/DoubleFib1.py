from files.helper.builder.OrderBuilder import OrderBuilder
from files.helper.builder.TradeBuilder import TradeBuilder
from files.helper.calculator.PositionSizeCalculator import PositionSizeCalculator
from files.helper.mediator.PriceMediator import PriceMediator
from files.interfaces.ITimeWindow import ITimeWindow
from files.models.asset.Candle import Candle
from files.models.asset.Relation import Relation
from files.models.frameworks.FrameWork import FrameWork
from files.models.frameworks.time.NYOpen import NYOpen
from files.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from files.models.strategy.Strategy import Strategy
from files.models.strategy.Result import StrategyResult
from files.models.strategy.ResultStatus import StrategyResultStatusEnum
from files.models.trade.Trade import Trade
from files.models.trade.enums.Side import Side
from files.models.trade.enums.TriggerBy import TriggerBy
from files.models.trade.enums.TriggerDirection import TriggerDirection

# Double Fib

class DoubleFib1(Strategy):

    def __init__(self, ):
        self.name = "DoubleFib1"
        self.timeframes = []

        self.timeframes.append(ExpectedTimeFrame(timeframe=1, max_len=90))

        self._timewindow: ITimeWindow = NYOpen()
        self._order_builder = OrderBuilder()
        self._trade_builder = TradeBuilder()
        self.time_windows = []
        self._price_mediator: PriceMediator = PriceMediator()
        self._risk_calculator: PositionSizeCalculator = PositionSizeCalculator()

    def entry(self, candles: list[Candle], timeFrame: int, relation: Relation, asset_class: str) -> StrategyResult:

        if len(candles) >= 0:
            self._price_mediator.analyze(first_candle=candles[-3], second_candle=candles[-2],
                                         third_candle=candles[-1]
                                         , timeframe=timeFrame)
        else:
            return StrategyResult()

        if candles and timeFrame == 1:

            third_candle: Candle = candles[-1]
            second_candle: Candle = candles[-2]
            first_candle: Candle = candles[-3]

            time = third_candle.iso_time

            bos = self._price_mediator.get_bos(timeFrame)

            imbalances = self._price_mediator.get_imbalances(timeFrame)

            if len(imbalances) > 900 or third_candle.iso_time.day != second_candle.iso_time.day:
                self._price_mediator.reset()

            if not bos or not imbalances:
                return StrategyResult()

            levels = self._price_mediator.get_fibonnaci(bos.candles, ote=True)

            levels.extend(self._price_mediator.get_fibonnaci(bos.candles, pd=True))

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
            stop = first_candle.close
            take_profit = first_candle.high
            order_dir = Side.BUY.value
            exit_dir = Side.SELL.value
            profit_dir = TriggerDirection.RISE.value
            stop_dir = TriggerDirection.FALL.value

            if fib_levels["fib_low"] < third_candle.close < fib_levels["fib_high"]:
                if bos.direction == "Bullish" and fib_levels["bullish_low_ote"] < third_candle.close < fib_levels["bullish_high_ote"]:
                    stop = fib_levels["fib_bullish_tp"]
                    take_profit = fib_levels["fib_bearish_tp"]
                    order_dir = Side.BUY.value
                    exit_dir = Side.SELL.value
                    profit_dir = TriggerDirection.RISE.value
                    stop_dir = TriggerDirection.FALL.value
                if bos.direction == "Bearish" and fib_levels["bearish_low_ote"] < third_candle.close < fib_levels["bearish_high_ote"]:
                    stop = fib_levels["fib_bearish_tp"]
                    take_profit = fib_levels["fib_bullish_tp"]
                    order_dir = Side.SELL.value
                    exit_dir = Side.BUY.value
                    profit_dir = TriggerDirection.FALL.value
                    stop_dir = TriggerDirection.RISE.value

            if not self.is_in_time(time):
                 return StrategyResult()

            if order_dir:

                trade = self._create_trade(relation=relation, order_dir=order_dir
                                           , exit_dir=exit_dir, profit_dir=profit_dir
                                           , stop_dir=stop_dir, take_profit=take_profit
                                           , stop=stop, last_candle=third_candle
                                           , asset_class=asset_class, levels=[])

                return StrategyResult(trade=trade, status=StrategyResultStatusEnum.NEWTRADE.value)
            else:
                return StrategyResult()
        else:
            return StrategyResult()

    def exit(self, candles: list, timeFrame: int, trade: Trade, relation: Relation) -> StrategyResult:
        # todo seperate entry exit / price mediator decoupling / create trade decoupling / risk management from outer
        # todo daily updater for risk profile and mediator
        # todo smt
        # todo faker exit test
        # todo test price mediator
        # todo implement strategies + test
        # todo trail stop
        # todo entry exit swap +  ui strategy builder for backtest
        return StrategyResult(trade=trade, status=StrategyResultStatusEnum.NOCHANGE.value)

    def _create_trade(self, relation: Relation, order_dir: str, exit_dir: str, stop_dir: str
                      , profit_dir: str, take_profit: float, stop: float, last_candle: Candle, asset_class: str,
                      levels: list[FrameWork]):

        trade = self._trade_builder.create_trade(relation=relation, category=relation.category, orders=[],
                                                 side=order_dir).build()

        entry_order = self._order_builder.create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                       , category=relation.category, side=order_dir
                                                       , risk_percentage=1
                                                       , order_number=1,
                                                       tradeId=trade.trade_id).build()

        stop_order = self._order_builder.create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                      , category=relation.category, side=exit_dir
                                                      , risk_percentage=1
                                                      , order_number=2
                                                      , tradeId=trade.trade_id).set_conditional(
            trigger_direction=stop_dir
            , trigger_price=stop, trigger_by=
            TriggerBy.MARKPRICE.value).set_defaults(price=stop).build()

        take_profit_order = OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                        , category=relation.category, side=exit_dir
                                                        , risk_percentage=1
                                                        , order_number=3
                                                        , tradeId=trade.trade_id).set_conditional(
            trigger_direction=profit_dir
            , trigger_price=take_profit
            , trigger_by=TriggerBy.MARKPRICE.value).set_defaults(price=take_profit).build()

        qty = str(self._risk_calculator.calculate_order_qty(asset_class=asset_class
                                                            , entry_price=float(last_candle.close)
                                                            , exit_price=float(stop_order.price)))

        entry_order.qty = qty # todo instead qty use risk % auslagern nach risk manager
        take_profit_order.qty = qty #  damit risk manager risk profile verwendet für beredchnung
        stop_order.qty = qty

        trade.orders.append(entry_order)
        trade.orders.append(stop_order)
        trade.orders.append(take_profit_order)

        return trade

    @staticmethod
    def _get_fibonacci_levels(levels) -> tuple[dict, list]:
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