import random
from collections import deque

from files.models.asset.Candle import Candle
from files.models.asset.CandleSeries import CandleSeries
from files.models.asset.Relation import Relation
from files.models.backtest.TradeResult import TradeResult
from files.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from files.models.strategy.OrderResultStatusEnum import OrderResultStatusEnum
from files.models.strategy.Strategy import Strategy
from files.models.strategy.StrategyResult import StrategyResult
from files.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from files.models.trade.Order import Order
from files.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from files.models.trade.enums.OrderTypeEnum import OrderTypeEnum
from files.models.trade.enums.TriggerDirectionEnum import TriggerDirection
from files.monitoring.logging.logging_startup import logger

class TestModule:
    def __init__(self,asset_class:str,strategy:Strategy, asset:str,candles:list[Candle]
                 , timeframes:list[ExpectedTimeFrame],trade_limit:int=2):
        self.asset = asset
        self.asset_class = asset_class
        self.strategy = strategy
        self.candles = candles
        self.timeframes = timeframes
        self._trade_que = deque(maxlen=trade_limit) # list of tradeIds
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

                    try:
                        result = self.strategy.get_entry(candles=series
                                                             ,timeFrame=candle.timeframe
                                                             ,relation=fake_relation,asset_class=self.asset_class)

                        if result.status == StrategyResultStatusEnum.NEWTRADE.value and len(self._trade_que) < self._trade_que.maxlen:
                            self.handle_new_trade(result, series[-1])
                    except Exception as e:
                        logger.debug("Testing Strategy Entry Failed,Error{e}".format(e=e))
                    if self.results:
                        self.handle_exits(series)

        self.calculate_trade_results()


    def handle_new_trade(self,result:StrategyResult,last_candle:Candle):
        trade_result = TradeResult(tradeId=result.trade.tradeId
                                   , filled_orders=[], active_orders=[], pending_orders=[], deleted_orders=[])
        self.trade_results[result.trade.tradeId] = trade_result
        updated_result = self._update_trade_results(result, last_candle)
        self.results[updated_result.trade.tradeId] = updated_result
        self._trade_que.append(updated_result.trade.tradeId)

    def handle_exits(self,series:list[Candle]):
        last_candle = series[-1]

        finished_ids = []

        for id in self._trade_que:
            try:
                result = self.results[id]
                strategy_result = self.strategy.get_exit(candles=series,
                                                                      timeFrame=last_candle.timeframe,
                                                                      relation=result.trade.relation,
                                                                      trade=result.trade)

                updated_result = self._update_trade_results(strategy_result, last_candle)

                self.results[result.trade.tradeId] = updated_result

                trade_result = self.trade_results[id]

                if trade_result.is_closed:
                    finished_ids.append(id)

            except Exception as e:
                logger.error("Testing Strategy Entry Failed,Error{e}".format(e=e))
                finished_ids.append(id)
                continue

        for id in finished_ids:
            self._trade_que.remove(id)

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
                if order.side == OrderDirectionEnum.BUY.value:
                    total_qty += order_qty

                if order.side == OrderDirectionEnum.SELL.value:
                    total_qty -= order_qty

                highest_price = max(highest_price, float(order.price))
                lowest_price = min(lowest_price, float(order.price))

            for order in trade_result.pending_orders:
                if order.price:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))
                if order.triggerPrice and order.orderType == OrderTypeEnum.MARKET.value:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))

            for order in trade_result.active_orders:
                if order.price:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))
                if order.triggerPrice and order.orderType == OrderTypeEnum.MARKET.value:
                    highest_price = max(highest_price, float(order.price))
                    lowest_price = min(lowest_price, float(order.price))

            # Sortiere Orders nach Zeit
            trade_result.filled_orders.sort(key=lambda x: x.createdTime)

            # Entry & Exit Zeiten setzen
            trade_result.entry_time = trade_result.filled_orders[0].createdTime
            trade_result.exit_time = trade_result.filled_orders[-1].createdTime

            # Exit-Preis ist der Preis der letzten Order
            exit_price = float(trade_result.filled_orders[-1].price)

            if trade_result.qty != 0:
                exit_price = trade_result.last_candle.close

            # PnL Berechnung
            if trade_result.side == OrderDirectionEnum.BUY.value:
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
    def _get_execution_price(last_candle, order_side)->float:
        """
        Simulate market order execution price with potential slippage.
        """
        slippage_pct = random.uniform(0, 0.00045)  # Example: Up to 0.05% slippage

        if order_side == OrderDirectionEnum.BUY.value:
            return last_candle.low * (1 + slippage_pct)  # Buy fills slightly higher
        elif order_side == OrderDirectionEnum.SELL.value:
            return last_candle.high * (1 - slippage_pct)  # Sell fills slightly lower
        return last_candle.close  # Default to last price if no slippage

    @staticmethod
    def _check_conditional_order(order: Order, last_candle: Candle)->bool:
        if order.triggerDirection:
            if order.triggerDirection == TriggerDirection.FALL.value and last_candle.low <= float(order.triggerPrice):
                return True

            if order.triggerDirection == TriggerDirection.RISE.value and last_candle.high >= float(order.triggerPrice):
                return True
        return False

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

    def _set_entry_(self, order: Order, trade_result: TradeResult, last_candle: Candle):
        if trade_result.entry_price == 0.0:
            trade_result.side = order.side
            trade_result.entry_price = self._get_execution_price(last_candle, order.side)  # Simulate Slippage
            trade_result.entry_time = str(last_candle.iso_time)

    def _create_tp_sl_order(self,order:Order)->list[Order]:
        new_orders = []
        if order.takeProfit:
            if order.tpLimitPrice:
                limit_order:Order = self._create_limit_exit_order(order=order,is_stop=False)
                new_orders.append(limit_order)
            else:
                market_order:Order = self._create_market_exit_order(order=order,is_stop=False)
                new_orders.append(market_order)
        if order.stopLoss:
            if order.slLimitPrice:
                limit_order:Order = self._create_limit_exit_order(order=order,is_stop=True)
                new_orders.append(limit_order)
            else:
                market_order:Order = self._create_market_exit_order(order=order,is_stop=True)
                new_orders.append(market_order)
        return new_orders

    def _execute_market_order(self,order:Order, trade_result:TradeResult, last_candle:Candle):
        if order.side == OrderDirectionEnum.BUY.value:
            trade_result.qty += float(order.qty) # Increase long position
        elif order.side == OrderDirectionEnum.SELL.value:
            trade_result.qty -= float(order.qty)  # Increase short position

        order.price = str(self._get_execution_price(last_candle, order.side))
        order.createdTime = str(last_candle.iso_time)

        if trade_result.entry_price == 0.0:
            self._set_entry_(order, trade_result, last_candle)

        trade_result.filled_orders.append(order)

    def _execute_limit_order(self,order:Order, trade_result:TradeResult, last_candle:Candle)->bool:
        if order.side == OrderDirectionEnum.BUY.value and float(order.price) <= last_candle.high:
            trade_result.qty += float(order.qty)  # Increase long position
            trade_result.filled_orders.append(order)
            order.createdTime = str(last_candle.iso_time)

            self._set_entry_(order, trade_result, last_candle)
            return True
        if order.side == OrderDirectionEnum.SELL.value and float(order.price) >= last_candle.low:
            trade_result.qty -= float(order.qty)
            trade_result.filled_orders.append(order)
            order.createdTime = str(last_candle.iso_time)

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

        trade_result.last_candle = last_candle

        trade_result.highest_price = max(last_candle.high, trade_result.highest_price)
        trade_result.lowest_price = min(last_candle.low, trade_result.lowest_price)

        tp_sl_orders = []
        remove_orders = set()  # Track orders that need to be removed

        for order in strategy_result.trade.orders:

            update_order = True

            while update_order:

                filled_orders = {o.orderLinkId for o in trade_result.filled_orders}
                active_orders = {o.orderLinkId for o in trade_result.active_orders}
                pending_orders = {o.orderLinkId for o in trade_result.pending_orders}
                update_order = False

                if order.orderLinkId in filled_orders:
                    continue

                if order.order_result_status == OrderResultStatusEnum.CLOSE.value:
                    if order.orderLinkId not in trade_result.deleted_orders:
                        trade_result.deleted_orders.append(order)
                    if order.orderLinkId not in remove_orders:
                        remove_orders.add(order.orderLinkId)

                if order.orderLinkId in active_orders:
                    if self._handle_active_order(order, trade_result, last_candle):
                        trade_result.active_orders = [o for o in trade_result.active_orders if
                                                      o.orderLinkId != order.orderLinkId]
                        if trade_result.qty == 0.0:
                            trade_result.exit_time = str(last_candle.iso_time)
                            trade_result.is_closed = True
                            continue

                if order.orderLinkId in pending_orders:
                    if self._check_conditional_order(order, last_candle):
                        if order.takeProfit or order.stopLoss:
                            tp_sl_orders.extend(self._create_tp_sl_order(order))
                        trade_result.active_orders.append(order)
                        trade_result.pending_orders = [o for o in trade_result.pending_orders if
                                                      o.orderLinkId != order.orderLinkId]
                        update_order = True
                    continue

                if order.triggerDirection or order.triggerPrice:
                    trade_result.pending_orders.append(order)
                    update_order = True
                    continue
                if order.takeProfit or order.stopLoss:
                    tp_sl_orders.extend(self._create_tp_sl_order(order))
                if order.orderType == OrderTypeEnum.MARKET.value:
                    self._execute_market_order(order, trade_result, last_candle)
                    continue
                if order.orderType == OrderTypeEnum.LIMIT.value:
                    if self._execute_limit_order(order, trade_result, last_candle):
                        update_order = True
                        continue
                    else:
                        update_order = True
                        trade_result.active_orders.append(order)

        trade_result.pending_orders = [o for o in trade_result.pending_orders if o.orderLinkId not in remove_orders]
        trade_result.active_orders = [o for o in trade_result.active_orders if o.orderLinkId not in remove_orders]
        strategy_result.trade.orders.extend(tp_sl_orders)

        return strategy_result