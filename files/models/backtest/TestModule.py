from logging import Logger

from collections import deque

from files.helper.mediator.PriceMediator import PriceMediator
from files.models.asset.Candle import Candle
from files.models.asset.CandleSeries import CandleSeries
from files.models.backtest.FakeBroker import FakeBroker
from files.models.backtest.TradeResult import TradeResult
from files.models.strategy.EntryInput import EntryInput
from files.models.strategy.ExitInput import ExitInput
from files.models.strategy.Strategy import Strategy
from files.models.strategy.Result import StrategyResult
from files.models.trade.Order import Order
from files.models.trade.enums.OrderResultStatusEnum import OrderResultStatusEnum
from files.models.trade.enums.Side import Side
from files.models.trade.enums.OrderType import OrderType
from files.models.trade.enums.StrategyResultStatusEnum import StrategyResultStatusEnum


class TestModule:
    def __init__(self,asset_class:str,strategy:Strategy, asset:str,candles:list[Candle]
                 ,logger:Logger,trade_limit:int=2,):
        self.asset = asset
        self.asset_class = asset_class
        self.strategy = strategy
        self.candles = candles
        self.trade_que = deque(maxlen=trade_limit) # list of tradeIds
        self.fake_broker = FakeBroker()
        self.mediator = PriceMediator()
        self.logger = logger
        self.results:dict[str,StrategyResult] = {}
        self.trade_results:dict[str,TradeResult] = {}

    def start_module(self):

        candles_series:list[CandleSeries] = self._prepare_candle_series()

        for candle in self.candles:
            for serie in candles_series:
                serie : CandleSeries = serie
                if serie.time_frame == candle.timeframe:

                    serie.candle_series.append(candle)

                    series = serie.to_list()

                    if len(series) >= 2:
                        continue

                    self.mediator.analyze(first_candle=candle[-1],second_candle=candle[-2],third_candle=candle[-3],timeframe=candle.timeframe)

                    try:
                        entry_input = EntryInput(candles=series,price_mediator=self.mediator)
                        result = self.strategy.entry_strategy.get_entry(entry_input)

                        if result.status == StrategyResultStatusEnum.NEWTRADE.value and len(self.trade_que) < self.trade_que.maxlen:
                            self.handle_new_trade(result, series[-1])
                    except Exception as e:
                        self.logger.error("Testing Strategy Entry Failed,Error{e}".format(e=e))
                    if self.results:
                        self.handle_exits(series)

        self.calculate_trade_results()

    def _prepare_candle_series(self)->list[CandleSeries]:
        timeframes = []
        candle_series:list[CandleSeries] = []
        for candle in self.candles:
            if candle.time_frame in timeframes:
                continue
            else:
                timeframes.append(candle.time_frame)
        for timeframe in timeframes:
            candle_series.append(CandleSeries(candle_series=deque(maxlen=200),time_frame=timeframe,broker=""))

        return candle_series

    def handle_new_trade(self,result:StrategyResult,last_candle:Candle):
        trade_result = TradeResult(trade_id=result.trade.trade_id
                                   , filled_orders=[], active_orders=[], pending_orders=[], deleted_orders=[])
        self.trade_results[result.trade.trade_id] = trade_result
        updated_result = self._update_trade_results(result, last_candle)
        self.results[updated_result.trade.trade_id] = updated_result
        self.trade_que.append(updated_result.trade.trade_id)

    def handle_exits(self,series:list[Candle]):
        last_candle = series[-1]

        finished_ids = []

        for id in self.trade_que:
            try:
                result:StrategyResult = self.results[id]

                exit_input = ExitInput(trade=result.trade,candles=series,mediator=self.mediator)

                strategy_result = self.strategy.exit_strategy.get_exit(exit_input)

                updated_result = self._update_trade_results(strategy_result, last_candle)

                self.results[result.trade.trade_id] = updated_result

                trade_result = self.trade_results[id]

                if trade_result.is_closed:
                    finished_ids.append(id)

            except Exception as e:
                self.logger.error("Testing Strategy Entry Failed,Error{e}".format(e=e))
                finished_ids.append(id)
                continue

        for id in finished_ids:
            self.trade_que.remove(id)

    def calculate_trade_results(self):
        for trade_result in self.trade_results.values():

            trade_result : TradeResult = trade_result

            if not trade_result.filled_orders:
                continue  # Kein gefüllter Trade → Überspringen

            # Initiale Variablen
            total_qty = 0.0
            highest_price: float = float('-inf')
            lowest_price: float = float('inf')
            max_drawdown = 0.0

            if trade_result.entry_price == 0.0:
                continue

            # Iteriere über alle gefüllten Orders
            for order in trade_result.filled_orders:
                order_qty = float(order.qty)

                # Berechne Gesamtmenge (positiv für BUY, negativ für SELL)
                if order.side == Side.BUY.value:
                    total_qty += order_qty

                if order.side == Side.SELL.value:
                    total_qty -= order_qty

                highest_price = max(highest_price, float(order.price))
                lowest_price = min(lowest_price, float(order.price))

            for order in trade_result.pending_orders:
                if order.price:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))
                if order.trigger_price and order.order_type == OrderType.MARKET.value:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))

            for order in trade_result.active_orders:
                if order.price:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))
                if order.trigger_price and order.order_type == OrderType.MARKET.value:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))

            # Sortiere Orders nach Zeit
            trade_result.filled_orders.sort(key=lambda x: x.created_time)

            # Entry & Exit Zeiten setzen
            trade_result.entry_time = trade_result.filled_orders[0].created_time
            trade_result.exit_time = trade_result.filled_orders[-1].created_time

            # Exit-Preis ist der Preis der letzten Order
            exit_price = float(trade_result.filled_orders[-1].price)

            if trade_result.qty != 0:
                exit_price = trade_result.last_candle.close

            # PnL Berechnung
            if trade_result.side == Side.BUY.value:
                trade_result.pnl_percentage = ((exit_price - trade_result.entry_price) / trade_result.entry_price) * 100
                max_drawdown = ((trade_result.entry_price - trade_result.lowest_price) / trade_result.entry_price) * 100
                trade_result.stop = lowest_price
                trade_result.take_profit = highest_price
            else:
                trade_result.pnl_percentage = ((trade_result.entry_price - exit_price) / trade_result.entry_price) * 100
                max_drawdown = ((trade_result.highest_price - trade_result.entry_price) / trade_result.entry_price) * 100
                trade_result.stop = highest_price
                trade_result.take_profit = lowest_price

            trade_result.max_drawdown = max_drawdown

    def _set_entry_(self, order: Order, trade_result: TradeResult, last_candle: Candle):
        if trade_result.entry_price == 0.0:
            trade_result.side = order.side
            trade_result.entry_price = self.fake_broker.get_execution_price(last_candle, order.side)  # Simulate Slippage
            trade_result.entry_time = str(last_candle.iso_time)

    def _execute_market_order(self, order:Order, trade_result:TradeResult, last_candle:Candle):
        if order.side == Side.BUY.value:
            trade_result.qty += float(order.qty) # Increase long position
        elif order.side == Side.SELL.value:
            trade_result.qty -= float(order.qty)  # Increase short position

        order.price = str(self.fake_broker.get_execution_price(last_candle, order.side))
        order.created_time = str(last_candle.iso_time)

        self._set_entry_(order, trade_result, last_candle)

        trade_result.filled_orders.append(order)

    def _execute_limit_order(self, order:Order, trade_result:TradeResult, last_candle:Candle)->bool:
        if order.side == Side.BUY.value and float(order.price) <= last_candle.high:
            trade_result.qty += float(order.qty)  # Increase long position
            trade_result.filled_orders.append(order)
            order.created_time = str(last_candle.iso_time)

            self._set_entry_(order, trade_result, last_candle)
            return True
        if order.side == Side.SELL.value and float(order.price) >= last_candle.low:
            trade_result.qty -= float(order.qty)
            trade_result.filled_orders.append(order)
            order.created_time = str(last_candle.iso_time)

            self._set_entry_(order, trade_result, last_candle)
            return True
        return False

    def _handle_active_order(self,order, trade_result, last_candle):
        if order.order_type == OrderType.LIMIT.value:
            if self._execute_limit_order(order, trade_result, last_candle):

                return True
        elif order.order_type == OrderType.MARKET.value:
            self._execute_market_order(order, trade_result, last_candle)

            return True
        return False

    def _update_trade_results(self, strategy_result: StrategyResult, last_candle: Candle)->StrategyResult:
        trade_result:TradeResult = self.trade_results[strategy_result.trade.trade_id]

        if trade_result.is_closed or strategy_result.status == StrategyResultStatusEnum.CLOSE.value:
            trade_result.is_closed = True
            return strategy_result

        trade_result.last_candle = last_candle

        trade_result.highest_price = max(last_candle.high, trade_result.highest_price)
        trade_result.lowest_price = min(last_candle.low, trade_result.lowest_price)

        tp_sl_orders = []
        remove_orders = set()  # Track orders that need to be removed

        for order in strategy_result.trade.orders:

            update_order = True

            while update_order:

                filled_orders = {o.order_link_id for o in trade_result.filled_orders}
                active_orders = {o.order_link_id for o in trade_result.active_orders}
                pending_orders = {o.order_link_id for o in trade_result.pending_orders}
                update_order = False

                if order.order_link_id in filled_orders:
                    continue

                if order.order_result_status == OrderResultStatusEnum.CLOSE.value:
                    if order.order_link_id not in trade_result.deleted_orders:
                        trade_result.deleted_orders.append(order)
                    if order.order_link_id not in remove_orders:
                        remove_orders.add(order.order_link_id)

                if order.order_link_id in active_orders:
                    if self._handle_active_order(order, trade_result, last_candle):
                        trade_result.active_orders = [o for o in trade_result.active_orders if
                                                      o.order_link_id != order.order_link_id]
                        if trade_result.qty == 0.0:
                            trade_result.exit_time = str(last_candle.iso_time)
                            trade_result.is_closed = True
                            continue

                if order.order_link_id in pending_orders:
                    if self.fake_broker.check_conditional_order(order.trigger_direction, order.trigger_price, last_candle):
                        if order.take_profit or order.stop_loss:
                            tp_sl_orders.extend(self.fake_broker.create_tp_sl_order(order))
                        trade_result.active_orders.append(order)
                        trade_result.pending_orders = [o for o in trade_result.pending_orders if
                                                       o.order_link_id != order.order_link_id]
                        update_order = True
                    continue

                if order.trigger_direction or order.trigger_price:
                    trade_result.pending_orders.append(order)
                    update_order = True
                    continue
                if order.take_profit or order.stop_loss:
                    tp_sl_orders.extend(self.fake_broker.create_tp_sl_order(order))
                if order.order_type == OrderType.MARKET.value:
                    self._execute_market_order(order, trade_result, last_candle)
                    continue
                if order.order_type == OrderType.LIMIT.value:
                    if self._execute_limit_order(order, trade_result, last_candle):
                        update_order = True
                        continue
                    else:
                        update_order = True
                        trade_result.active_orders.append(order)

        trade_result.pending_orders = [o for o in trade_result.pending_orders if o.order_link_id not in remove_orders]
        trade_result.active_orders = [o for o in trade_result.active_orders if o.order_link_id not in remove_orders]
        strategy_result.trade.orders.extend(tp_sl_orders)

        return strategy_result