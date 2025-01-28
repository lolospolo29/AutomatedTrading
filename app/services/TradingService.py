import threading
from typing import Any, Dict

from app.manager.AssetManager import AssetManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade
from app.monitoring.log_time import log_time
from app.monitoring.logging.logging_startup import logger
from app.services.NewsService import NewsService


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

    :ivar _asset_manager: Manages and tracks assets and their data.
    :type _asset_manager: AssetManager
    :ivar _trade_manager: Manages trade execution, amendments, and archival.
    :type _trade_manager: TradeManager
    :ivar _strategy_manager: Executes and evaluates trading strategies.
    :type _strategy_manager: StrategyManager
    :ivar _news_service: Handles news-related events, implications, or constraints in trading.
    :type _news_service: NewsService
    :ivar news_event_ahead_counter: Counter to track the number of encountered news events ahead.
    :type news_event_ahead_counter: int
    :ivar _logger: Logger instance for auditing and operational monitoring.
    :type _logger: Logger
    :ivar _initialized: Internal state flag for service initialization.
    :type _initialized: bool
    """
    # region Singleton

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradingService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # endregion

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._asset_manager: AssetManager = AssetManager()
            self._trade_manager: TradeManager = TradeManager()
            self._strategy_manager: StrategyManager = StrategyManager()
            self._news_service :NewsService = NewsService()
            #self._news_service.receive_news()
            self.news_event_ahead_counter = 0
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
        candle: Candle = self._asset_manager.add_candle(jsonData)

        logger.debug("Received candle for Asset:{asset},{timeframe}".format(asset=candle.asset, timeframe=candle.timeframe))

        candles : list[Candle] = self._asset_manager.return_candles(candle.asset, candle.broker, candle.timeframe)

        is_news_ahead,message = self._news_service.receive_news()

        if not is_news_ahead:

            relations: list[AssetBrokerStrategyRelation] = self._asset_manager.return_relations(candle.asset, candle.broker)

            logger.debug("Processing: {candle}, {relations}".format(candle=candle, relations=relations))
            threads:list[threading.Thread] = []
            for relation in relations:
                thread = threading.Thread(target=self._process_relation_strategy,
                                          args=(candle.timeframe,candles,relation), daemon=True)
                threads.append(thread)
            for thread in threads:
                thread.start()

        elif is_news_ahead:
            self.news_event_ahead_counter += 1
            if self.news_event_ahead_counter % 10 == 0:
                self._logger.info(message)


    def _process_relation_strategy(self, timeframe:int, candles:list[Candle], relation:AssetBrokerStrategyRelation):
        """
        Processes the trading strategy for a specific relation, determining whether to enter new trades
        or manage existing trades concurrently.

        Args:
            timeframe (int): The timeframe for the analysis (e.g., minutes, hours).
            candles (list[Candle]): A list of candle objects representing market data.
            relation (AssetBrokerStrategyRelation): The relation object linking the asset and strategy.

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
                thread = threading.Thread(target=self._analyze_strategy_for_entry,
                                          args=(timeframe,candles,relation,trade), daemon=True)
                threads.append(thread)
            for thread in threads:
                thread.start()

    @log_time
    def _analyze_strategy_for_entry(self, timeframe:int, candles:list[Candle], relation:AssetBrokerStrategyRelation) -> None:
        """
        Analyses Strategy Logic.
        If there is a Signal for Entry,the Strategy generates a Trade Object.
        That Object is used to Execute Orders in the Trade Manager.

        :param timeframe: Timeframe to analyse.
        :param candles: Candles to analyse.
        """

        result: StrategyResult = self._strategy_manager.get_entry(candles, relation, timeframe)

        if result.status.NEWTRADE.value:
            self._logger.info(f"New Entry found: {relation.asset}")

            self._trade_manager.register_trade(result.trade)
            exceptionOrders,trade = self._trade_manager.place_trade(result.trade)
            self._trade_manager.update_trade(trade)

            if exceptionOrders:
                self._closing_trade(result.trade)

    def _analyze_strategy_for_exit(self,timeframe:int, candles:list[Candle], relation:AssetBrokerStrategyRelation,trade:Trade)->None:
        """
        Analyzes the trading strategy to determine if an exit condition is met for a given trade.

        Args:
            timeframe (int): The timeframe for the analysis (e.g., minutes, hours).
            candles (list[Candle]): A list of candle objects representing market data.
            relation (AssetBrokerStrategyRelation): The relation object linking the asset and strategy.
            trade (Trade): The trade object to evaluate for exit conditions.

        Behavior:
            - Evaluates the exit conditions for the given trade using the strategy manager.
            - Handles two exit statuses:
                1. **CLOSE**: Logs the close action and invokes the `_closing_trade` method to close the trade.
                2. **CHANGED**: Logs the change action, attempts to amend the trade, and updates the trade if modifications are successful.
                   If there are issues with the orders (`exceptionOrders`), the trade is closed.

        Notes:
            - Uses `self._strategy_manager.get_exit` to retrieve the exit strategy result.
            - The `_closing_trade` method is used to close the trade.
            - The trade amendments are managed through the `self._trade_manager.amend_trade` method.

        Logging:
            - Logs information about detected "Close" or "Changed" exit conditions along with the related asset.

        Returns:
            None
        """
        result: StrategyResult = self._strategy_manager.get_exit(candles, relation, timeframe,trade)

        if result.status.CLOSE.value:
            self._logger.info(f"Close Exit found: {relation.asset}")
            self._trade_manager.update_trade(result.trade)
            self._closing_trade(result.trade)

        if result.status.CHANGED.value:
            self._logger.info(f"Changed Exit found: {relation.asset}")

            exceptionOrders,trade = self._trade_manager.amend_trade(result.trade)
            self._trade_manager.update_trade(trade)
        if result.status.NOCHANGE.value and timeframe >= 5:
            self._trade_manager.update_trade(trade)

    def _closing_trade(self,trade:Trade)->None:

        exceptionOrders, trade = self._trade_manager.cancel_trade(trade)
        trade = self._trade_manager.update_trade(trade)
        self._trade_manager.archive_trade(trade)
        self._logger.info(f"Canceled Trade: TradeId:{trade.id},"
                             f"Symbol:{trade.relation.asset},Broker:{trade.relation.broker},Pnl:{trade.unrealisedPnl}")
            # todo testing
            # todo testing module
            # todo execptions handling,exceptions
