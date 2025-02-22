from collections import deque

from app.models.asset.Candle import Candle
from app.models.asset.CandleSeries import CandleSeries
from app.models.asset.Relation import Relation
from app.models.backtest.TradeResult import TradeResult
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from app.models.trade.Trade import Trade
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.models.trade.enums.OrderTypeEnum import OrderTypeEnum


class TestModule:
    def __init__(self, strategy:Strategy, candles:list[Candle], timeframes:list[ExpectedTimeFrame],result_id:str):
        self.strategy = strategy
        self.candles = candles
        self.timeframes = timeframes
        self.result_id = result_id
        self.results:dict[str,StrategyResult] = {}
        self.trade_results:dict[str,TradeResult] = {}

    def start_module(self):

        candles_series:list[CandleSeries] = self._prepare_candle_series(self.timeframes)

        fake_relation = Relation(asset="",broker="",strategy=self.strategy.name,max_trades=99,id=0)

        for candle in self.candles:
            for serie in candles_series:
                serie : CandleSeries = serie
                if serie.timeFrame == candle.timeframe:

                    serie.candleSeries.append(candle)

                    series = serie.to_list()

                    result = self.strategy.get_entry(candles=series
                                                         ,timeFrame=candle.timeframe
                                                         ,relation=fake_relation,asset_class="")

                    is_new_trade = False

                    last_candle = series[-1]

                    if result.status == StrategyResultStatusEnum.NEWTRADE.value:
                        self.results[result.trade.tradeId] = result
                        self._create_trade_result(result.trade,last_candle)
                        is_new_trade = True

                    if self.results and not is_new_trade:
                        for result in self.results.values():
                            result = self.strategy.model_copy().get_exit(candles=series, timeFrame=candle.timeframe,
                                                                         relation=result.trade.relation, trade=result.trade)
                            self._update_trade_results(result.trade,last_candle)

    @staticmethod
    def _prepare_candle_series(timeframes: list[ExpectedTimeFrame]) -> list[CandleSeries]:
        candle_series: list[CandleSeries] = []

        for timeframe in timeframes:
            is_found = False

            for serie in candle_series:
                if serie.timeFrame == timeframe.timeframe:
                    is_found = True
                    break

            if is_found:
                continue

            candle_series.append(CandleSeries(candleSeries=deque(maxlen=timeframe.max_Len)
                                              , timeFrame=timeframe.timeframe, broker=""))
        return candle_series

    def _create_trade_result(self, trade: Trade, last_candle: Candle):
        trade_result = TradeResult(tradeId=trade.tradeId)

        for order in trade.orders:
            if order.orderType == OrderTypeEnum.MARKET.value:
                trade_result.is_active = True
                trade_result.entry_price = last_candle.close
                trade_result.entry_time = str(last_candle.iso_time)
                trade_result.side = order.side

                if order.side == OrderDirectionEnum.BUY.value:
                    trade_result.qty += order.qty
                if order.side == OrderDirectionEnum.SELL.value:
                    trade_result.qty -= order.qty

        self.trade_results[trade.tradeId] = trade_result

    def _update_trade_results(self, trade: Trade, last_candle: Candle):
        trade_result = self.trade_results[trade.tradeId]

        for order in trade.orders:
            if order.orderType == OrderTypeEnum.LIMIT.value:
                pass