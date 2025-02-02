from app.helper.builder.OrderBuilder import OrderBuilder
from app.helper.builder.TradeBuilder import TradeBuilder
from app.helper.facade.StrategyFacade import StrategyFacade
from app.helper.handler.LevelHandler import LevelHandler
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from app.models.trade.Trade import Trade
from app.models.trade.enums.CategoryEnum import CategoryEnum
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.models.trade.enums.StopOrderTypeEnum import StopOrderTypeEnum


# Double Fib

class DoubleFib(Strategy):


    def __init__(self):
        name: str = "DoubleFib"

        self._strategy_handler = StrategyFacade()

        self._level_handler = LevelHandler()

        self.expectedTimeFrames = []

        timeFrame2 = ExpectedTimeFrame(1, 90)

        self.expectedTimeFrames.append(timeFrame2)

        super().__init__(name, self.expectedTimeFrames)

    def return_expected_time_frame(self) -> list:
        return self.expectedTimeFrames

    def is_in_time(self, time) -> bool:
        return True # todo later add only macros

    def _analyzeData(self, candles: list, timeFrame: int):
        if timeFrame == 1 and len(candles) > 60:
            ote = self._strategy_handler.LevelMediator.calculate_fibonacci(level_type="OTE", candles= candles, lookback=60)
            for level in ote:
                self._strategy_handler.level_handler.add_level(level)
            self._strategy_handler.level_handler.remove_level(candles,timeFrame)



    def get_entry(self, candles: list, timeFrame: int,relation:AssetBrokerStrategyRelation,asset_class:str) ->StrategyResult:
        self._analyzeData(candles, timeFrame)
        levels:list[Level] = self._strategy_handler.level_handler.return_levels()
        if candles and levels and timeFrame == 1:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            if not self.is_in_time(time):
                return StrategyResult()

            levels:list[Level] = levels[-4:]

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
            if bullish_ote_level_min <= last_candle.close <= bullish_ote_level_max:
                stop = min(profit_stop_entry)
                take_profit = max(profit_stop_entry)
                order_dir = OrderDirectionEnum.BUY.value

            if bearish_ote_level_min <= last_candle.close <= bearish_ote_level_max:
                stop = max(profit_stop_entry)
                take_profit = min(profit_stop_entry)
                order_dir = OrderDirectionEnum.SELL.value

            if order_dir:
                trade = TradeBuilder().add_side(side=order_dir).add_category(category=CategoryEnum.LINEAR.value).add_relation(
                    relation=relation).build()

                order = OrderBuilder().create_order(relation=relation, symbol=relation.asset, confirmations=levels
                                                    ,category=CategoryEnum.LINEAR.value, side=order_dir
                                                    ,risk_percentage=1
                                                    ,order_number=1
                                                    ,trade_id=trade.id).set_defaults(price=last_candle.close
                                                    ,take_profit=take_profit,stop_loss=stop).build()

                self._strategy_handler.position_size_calculator.calculate_qty(asset_class=asset_class, order=order)
                trade.add_order(order)
                return StrategyResult(trade=trade,status=StrategyResultStatusEnum.NEWTRADE.value)
            else:
                return StrategyResult()
        else:
            return StrategyResult()

    def get_exit(self, candles: list, timeFrame: int, trade:Trade,relation:AssetBrokerStrategyRelation)->StrategyResult:
        return StrategyResult()
