import random
from collections import deque

from app.models.asset.Candle import Candle
from app.models.asset.CandleSeries import CandleSeries
from app.models.asset.Relation import Relation
from app.models.backtest.TradeResult import TradeResult
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.OrderResultStatusEnum import OrderResultStatusEnum
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from app.models.trade.Order import Order
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.models.trade.enums.OrderTypeEnum import OrderTypeEnum
from app.models.trade.enums.TriggerDirectionEnum import TriggerDirection


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

                    if result.status == StrategyResultStatusEnum.NEWTRADE.value:
                        self.handle_new_trade(result,series[-1])

                    if self.results:
                        self.handle_exits(series)

        self.calculate_trade_results()

    def handle_new_trade(self,result:StrategyResult,last_candle:Candle):
        trade_result = TradeResult(tradeId=result.trade.tradeId
                                   , filled_orders=[], active_orders=[], pending_orders=[], deleted_orders=[])
        self.trade_results[result.trade.tradeId] = trade_result
        updated_result = self._update_trade_results(result, last_candle)
        self.results[updated_result.trade.tradeId] = updated_result

    def handle_exits(self,series:list[Candle]):
        updated_results = []

        last_candle = series[-1]

        for result in self.results.values():
            strategy_result = self.strategy.model_copy().get_exit(candles=series,
                                                                  timeFrame=last_candle.timeframe,
                                                                  relation=result.trade.relation,
                                                                  trade=result.trade)

            updated_result = self._update_trade_results(strategy_result, last_candle)
            updated_results.append(updated_result)

        for result in updated_results:
            self.results[result.trade.tradeId] = result

    def calculate_trade_results(self):
        for trade_result in self.trade_results.values():
            trade_result: TradeResult = trade_result
            pass

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

    @staticmethod
    def _get_execution_price(last_candle, order_side):
        """
        Simulate market order execution price with potential slippage.
        """
        slippage_pct = random.uniform(0, 0.0005)  # Example: Up to 0.05% slippage

        if order_side == OrderDirectionEnum.BUY.value:
            return last_candle.close * (1 + slippage_pct)  # Buy fills slightly higher
        elif order_side == OrderDirectionEnum.SELL.value:
            return last_candle.close * (1 - slippage_pct)  # Sell fills slightly lower
        return last_candle.close  # Default to last price if no slippage

    @staticmethod
    def _check_conditional_order(order: Order, last_candle: Candle)->bool:
        if order.triggerDirection:
            if order.triggerDirection == TriggerDirection.FALL and last_candle.low > order.triggerPrice:
                return False

            if order.triggerDirection == TriggerDirection.RISE and last_candle.high < order.triggerPrice:
                return False
        return True

    @staticmethod
    def _create_limit_exit_order(order:Order,is_stop:bool)->Order:
        o = Order()
        o.orderType = OrderTypeEnum.LIMIT.value
        o.orderLinkId = order.orderLinkId + str(random.randint(1, 10000))
        o.qty = order.qty
        if not is_stop:
            o.price = order.tpLimitPrice
        if is_stop:
            o.price = order.slLimitPrice

        if order.side == OrderDirectionEnum.BUY.value:
            o.side = OrderDirectionEnum.SELL.value
        if order.side == OrderDirectionEnum.SELL.value:
            o.side = OrderDirectionEnum.BUY.value
        return o

    @staticmethod
    def _create_market_exit_order(order:Order,is_stop:bool)->Order:
        o = Order()
        o.orderType = OrderTypeEnum.MARKET.value
        o.orderLinkId = order.orderLinkId + str(random.randint(1, 10000))
        o.qty = order.qty
        if not is_stop:
            o.triggerPrice = order.takeProfit
        if is_stop:
            o.triggerPrice = order.stopLoss

        if order.side == OrderDirectionEnum.BUY.value:
            o.side = OrderDirectionEnum.SELL.value
        if order.side == OrderDirectionEnum.SELL.value:
            o.side = OrderDirectionEnum.BUY.value
        return o

    def _set_entry_(self,order:Order, trade_result:TradeResult, last_candle:Candle):
        if trade_result.entry_price is 0.0:
            trade_result.side = order.side
            trade_result.entry_price = self._get_execution_price(last_candle, order.side)  # Simulate Slippage
            trade_result.entry_time = str(last_candle.iso_time)

    def _create_tp_sl_order(self,order:Order)->list[Order]:
        new_orders = []
        if order.takeProfit:
            if order.tpLimitPrice:
                limit_order = self._create_limit_exit_order(order=order,is_stop=False)
                new_orders.append(limit_order)
            else:
                market_order = self._create_market_exit_order(order=order,is_stop=False)
                new_orders.append(market_order)
        if order.stopLoss:
            if order.slLimitPrice:
                limit_order = self._create_limit_exit_order(order=order,is_stop=True)
                new_orders.append(limit_order)
            else:
                market_order = self._create_market_exit_order(order=order,is_stop=True)
                new_orders.append(market_order)
        return new_orders

    def _execute_market_order(self,order:Order, trade_result:TradeResult, last_candle:Candle):
        if order.side == OrderDirectionEnum.BUY.value:
            trade_result.qty += order.qty  # Increase long position
        elif order.side == OrderDirectionEnum.SELL.value:
            trade_result.qty -= order.qty  # Increase short position

        order.price = self._get_execution_price(last_candle, order.side)

        if trade_result.entry_price is 0.0:
            self._set_entry_(order, trade_result, last_candle)

        trade_result.filled_orders.append(order)

    def _execute_limit_order(self,order:Order, trade_result:TradeResult, last_candle:Candle)->bool:
        if order.side == OrderDirectionEnum.BUY.value and order.price <= last_candle.high:
            trade_result.qty += order.qty  # Increase long position
            trade_result.filled_orders.append(order)
            self._set_entry_(order, trade_result, last_candle)
            return True
        if order.side == OrderDirectionEnum.SELL.value and order.price >= last_candle.low:
            trade_result.qty -= order.qty
            trade_result.filled_orders.append(order)
            self._set_entry_(order, trade_result, last_candle)
            return True
        return False

    def _handle_active_order(self,order, trade_result, last_candle):
        if order.orderType == OrderTypeEnum.LIMIT.value:
            if self._execute_limit_order(order, trade_result, last_candle):
                return True
        elif order.orderType == OrderTypeEnum.MARKET.value:
            self._execute_market_order(order, trade_result, last_candle)
            return True
        return False

    def _update_trade_results(self, strategy_result: StrategyResult, last_candle: Candle)->StrategyResult:
        trade_result:TradeResult = self.trade_results[strategy_result.trade.tradeId]

        if trade_result.is_closed or strategy_result.status == StrategyResultStatusEnum.CLOSE.value:
            trade_result.is_closed = True
            return strategy_result

        filled_orders = {o.orderLinkId for o in trade_result.filled_orders}
        active_orders = {o.orderLinkId for o in trade_result.active_orders}
        pending_orders = {o.orderLinkId for o in trade_result.pending_orders}

        tp_sl_orders = []
        remove_orders = set()  # Track orders that need to be removed

        for order in strategy_result.trade.orders:

            if order.orderLinkId in filled_orders:
                continue

            if order.order_result_status == OrderResultStatusEnum.CLOSE.value:
                trade_result.deleted_orders.append(order)
                remove_orders.add(order.orderLinkId)

            if order.orderLinkId in active_orders:
                if self._handle_active_order(order, trade_result, last_candle):
                    trade_result.active_orders = [o for o in trade_result.active_orders if
                                                  o.orderLinkId != order.orderLinkId]
                    continue

            if order.orderLinkId in pending_orders:
                if self._check_conditional_order(order, last_candle):
                    if order.takeProfit or order.stopLoss:
                        tp_sl_orders.extend(self._create_tp_sl_order(order))
                    trade_result.active_orders.append(order)
                    trade_result.pending_orders = [o for o in trade_result.pending_orders if
                                                  o.orderLinkId != order.orderLinkId]
                    continue

            if order.triggerDirection or order.triggerPrice:
                trade_result.pending_orders.append(order)
                continue
            if order.takeProfit or order.stopLoss:
                tp_sl_orders.extend(self._create_tp_sl_order(order))
            if order.orderType == OrderTypeEnum.MARKET.value:
                self._execute_market_order(order, trade_result, last_candle)
                continue
            if order.orderType == OrderTypeEnum.LIMIT.value:
                if self._execute_limit_order(order, trade_result, last_candle):
                    continue
                else:
                    trade_result.active_orders.append(order)

        trade_result.pending_orders = [o for o in trade_result.pending_orders if o.orderLinkId not in remove_orders]
        trade_result.active_orders = [o for o in trade_result.active_orders if o.orderLinkId not in remove_orders]
        strategy_result.trade.orders.extend(tp_sl_orders)

        return strategy_result
