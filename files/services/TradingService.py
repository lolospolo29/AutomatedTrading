import threading
from logging import Logger
from typing import Any, Dict

from files.helper.manager.AssetManager import AssetManager
from files.helper.registry.StrategyRegistry import StrategyRegistry
from files.helper.manager.TradeManager import TradeManager
from files.mappers.AssetMapper import AssetMapper
from files.models.asset.Relation import Relation
from files.models.asset.Candle import Candle
from files.models.strategy.StrategyResult import StrategyResult
from files.models.strategy.StrategyResultStatusEnum import StrategyResultStatusEnum
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade
from files.models.trade.enums.OrderTypeEnum import OrderTypeEnum
from files.monitoring.log_time import log_time
from files.services.NewsService import NewsService
from files.services.TelegramService import TelegramService


class TradingService:
    """
    Manages the core trading operations, including price action signal handling, strategy evaluation,
    and trade management. This service acts as an intermediary between asset management, strategy
    execution, and trade execution layers in a trading platform.

    Provides functionality for:
    - Receiving price action signals and processing them through strategies.
    - Managing trades based on strategy outputs.
    - Handling entry and exit conditions for trades.

    Thread-safe Singleton instance ensures centralized service usage within the application.
    """
    # region Singleton

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(TradingService, cls).__new__(cls)
        return cls._instance

    # endregion

    # region Initializing

    def __init__(self, asset_manager:AssetManager, trade_manager:TradeManager
                 , strategy_registry:StrategyRegistry, news_service:NewsService, telegram_service:TelegramService, logger:Logger, asset_mapper:AssetMapper):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._asset_manager: AssetManager = asset_manager
            self._trade_manager: TradeManager = trade_manager
            self._strategy_registry: StrategyRegistry = strategy_registry
            self._asset_mapper = asset_mapper
            self._news_service :NewsService = news_service
            self._telegram_service = telegram_service
            self._logger = logger
            self._logger.info("TradingService initialized")
            self._initialized = True  # Markiere als initialisiert

    # endregion
    @log_time
    def handle_price_action_signal(self, jsonData: Dict[str, Any]) -> None:
        """
        Handles the Dataflow between Strategy Manager,Asset Manager and Trade Manager.

        :param jsonData: JSON Object from Any Price Signal Services.
        """
        candle:Candle = self._asset_mapper.map_tradingview_json_to_candle(jsonData)
        self._asset_manager.add_candle(candle)

        self._logger.debug("Received candle for Asset:{asset},{timeframe}".format(asset=candle.asset, timeframe=candle.timeframe))

        candles : list[Candle] = self._asset_manager.return_candles(candle.asset, candle.broker, candle.timeframe)

        is_news_ahead,message = self._news_service.is_news_ahead()

        if not is_news_ahead:

            relations: list[Relation] = self._asset_manager.return_relations(candle.asset, candle.broker)

            self._logger.debug("Processing: {candle}, {relations}".format(candle=candle, relations=relations))
            threads:list[threading.Thread] = []
            for relation in relations:
                thread = threading.Thread(target=self._process_relation_strategy,
                                          args=(candle.timeframe,candles,relation), daemon=True)
                threads.append(thread)
            for thread in threads:
                thread.start()


    def _process_relation_strategy(self, timeframe:int, candles:list[Candle], relation:Relation):
        """
        Processes the trading strategy for a specific relation, determining whether to enter new trades
        or manage existing trades concurrently.
        Behavior:
            - If there are no existing trades for the relation, analyzes the strategy for potential entry points.
            - If there are existing trades, spawns separate threads to analyze each trade in the context of the strategy.

        Threading:
            - For each existing trade, creates a separate thread to concurrently analyze the strategy with respect to that trade.
            - Threads are started in daemon mode to ensure they do not block program termination.
        """
        trades:list[Trade] = self._trade_manager.return_trades_for_relation(relation)

        if len(trades) == 0:
            self._analyze_strategy_for_entry(timeframe, candles, relation)
        if len(trades) > 0:
            threads = []

            for trade in trades:
                thread = threading.Thread(target=self._analyze_strategy_for_exit,
                                          args=(timeframe,candles,relation,trade), daemon=True)
                threads.append(thread)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(240)

    @log_time
    def _analyze_strategy_for_entry(self, timeframe:int, candles:list[Candle], relation:Relation) -> None:
        """
        Analyses Strategy Logic.
        If there is a Signal for Entry,the Strategy generates a Trade Object.
        That Object is used to Execute Orders in the Trade Manager.
        """
        asset_class = self._asset_manager.return_asset_class(relation.asset)


        result: StrategyResult = self._strategy_registry.get_entry(candles, relation, timeframe, asset_class)
        if result.status is None:
            return
        if result.status == StrategyResultStatusEnum.NEWTRADE.value:
            self._logger.info(f"New Trade found:{result.trade.relation}")

            self._trade_manager.register_trade(result.trade)
            exceptionOrders,trade = self._trade_manager.place_trade(result.trade)
            self._trade_manager.update_trade(trade)

            message = self._format_orders(trade.orders)
            self._telegram_service.send(f"New Trade: {message}")

            if exceptionOrders:
                self._closing_trade(result.trade)

    def _analyze_strategy_for_exit(self, timeframe:int, candles:list[Candle], relation:Relation, trade:Trade)->None:
        """
        Analyzes the trading strategy to determine if an exit condition is met for a given trade.

        Behavior:
            - Evaluates the exit conditions for the given trade using the strategy manager.
            - Handles two exit statuses:
                1. **CLOSE**: Logs the close action and invokes the `_closing_trade` method to close the trade.
                2. **CHANGED**: Logs the change action, attempts to amend the trade, and updates the trade if modifications are successful.
                   If there are issues with the orders (`exceptionOrders`), the trade is closed.
        """
        result: StrategyResult = self._strategy_registry.get_exit(candles, relation, timeframe, trade)

        if result.status is None:
            return
        if result.status == StrategyResultStatusEnum.CLOSE.value:
            self._logger.info(f"Closing Trade: {relation.asset}")
            self._trade_manager.update_trade(result.trade)
            self._closing_trade(result.trade)
            message = self._format_orders(trade.orders)
            self._telegram_service.send(f"Closing Trade: {message}")

        if result.status == StrategyResultStatusEnum.CHANGED.value:
            self._logger.info(f"Changed Trade: {relation.asset}")
            exceptionOrders,trade = self._trade_manager.amend_trade(result.trade)
            self._trade_manager.update_trade(trade)

            message = self._format_orders(trade.orders)
            self._telegram_service.send(f"Changed Trade: {message}")

        if result.status == StrategyResultStatusEnum.NOCHANGE.value:
            self._trade_manager.update_trade(trade)
        else:
            self._trade_manager.archive_trade(trade)

    def _closing_trade(self,trade:Trade)->None:

        exceptionOrders, trade = self._trade_manager.cancel_trade(trade)
        trade = self._trade_manager.update_trade(trade)
        self._trade_manager.archive_trade(trade)
        self._logger.info(f"Canceled Trade: TradeId:{trade.tradeId},"
                             f"Symbol:{trade.relation.asset},Broker:{trade.relation.broker},Pnl:{trade.unrealisedPnl}")
        message = self._format_orders(trade.orders)
        self._telegram_service.send(f"Cancelled Trade: {message}")

    @staticmethod
    def _format_orders(orders:list[Order])->str:
        """Format orders dynamically based on their type."""

        formatted_orders = []

        for order in orders:
            if order.orderType == OrderTypeEnum.MARKET.value:
                if order.takeProfit:
                    formatted_orders.append(f"TakeProfit: {order.takeProfit},Id:{order.orderLinkId}")
                if order.stopLoss:
                    formatted_orders.append(f"StopLoss: {order.stopLoss},Id:{order.orderLinkId}")
                if order.triggerPrice:
                    formatted_orders.append(f"TriggerPrice: {order.triggerPrice},Id:{order.orderLinkId}")
                formatted_orders.append(f"• Market Order: {order.side} @ {order.qty},Id:{order.orderLinkId}")
            elif order.orderType == OrderTypeEnum.LIMIT.value:
                formatted_orders.append(f"• Limit Order: {order.side} @ {order.qty} (Limit: {order.price}),Id:{order.orderLinkId}")

        return "\n".join(formatted_orders)

