import threading
import uuid
from datetime import datetime

from app.db.mongodb.BacktestRepository import BacktestRepository
from app.helper.factories.StrategyFactory import StrategyFactory
from app.models.asset.Candle import Candle
from app.models.backtest.BacktestInput import BacktestInput
from app.models.backtest.Result import Result
from app.models.backtest.TestModule import TestModule
from app.monitoring.logging.logging_startup import logger


class BacktestService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(BacktestService, cls).__new__(cls)
        return cls._instance

    def __init__(self, backtest_repository: BacktestRepository):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.__factory = StrategyFactory()
            self._backtest_repository = backtest_repository
            self._asset_selection: list[str] = []
            self._fetch_test_assets()
            self._initialized = True  # Markiere als initialisiert

    def start_backtesting_strategy(self, backtest_input: BacktestInput) -> Result:

        test_data: dict[str, list[Candle]] = self._prepare_test_data(backtest_input.test_assets)

        asset_classes: dict[str, str] = self._get_asset_classes(backtest_input.test_assets)

        strategy = self.__factory.return_strategy(backtest_input.strategy)

        result = Result(strategy=strategy.name, result_id=str(uuid.uuid4()))

        modules: list[TestModule] = []

        threads = []

        if strategy is None:
            logger.error(f"Strategy {strategy} not found in Backtest Service")
            return result

        for asset in backtest_input.test_assets:
            logger.info(f"Starting backtest for {asset}")

            module = TestModule(asset_classes[asset], strategy.model_copy(), asset
                                , test_data[asset], strategy.timeframes, result.result_id)
            modules.append(module)
            thread = threading.Thread(target=module.start_module())
            threads.append(thread)
            thread.start()

        self._wait_for_threads(threads)

        for module in modules:
            result = self._add_module_statistic_to_result(module, result)

        logger.info(f"Backtest for {strategy.name} finished,Result: {result},ResultId: {result.result_id}")
        logger.info(f"Writing Result to DB...,ResultId: {result.result_id}")
        self._backtest_repository.add_result(result)

        return result

    def get_asset_selection(self) -> list[str]:
        return self._asset_selection

    def get_test_results(self, strategy: str = None) -> list[Result]:
        if strategy:
            return self._backtest_repository.find_result_by_strategy(strategy)
        else:
            return self._backtest_repository.find_results()

    def add_test_data(self, candles: list[Candle]):
        for candle in candles:
            self._backtest_repository.add_candle(candle)

    @staticmethod
    def _add_module_statistic_to_result(module: TestModule, result: Result) -> Result:
        """Fügt die Statistiken eines TestModules zum übergeordneten Result hinzu."""

        total_pnl = 0.0
        total_win_pnl = 0.0
        total_loss_pnl = 0.0
        total_win_count = 0
        total_loss_count = 0
        total_duration = 0.0
        max_drawdown = float('-inf')

        # Alle TradeResults aus dem TestModule iterieren
        for trade in module.trade_results.values():
            # Anzahl der Trades erhöhen
            result.no_of_trades += 1

            # Gewinn/Verlust berechnen
            total_pnl += trade.pnl_percentage
            max_drawdown = min(max_drawdown, trade.max_drawdown)  # Niedrigster Wert

            if trade.is_win:
                total_win_count += 1
                total_win_pnl += trade.pnl_percentage
            else:
                total_loss_count += 1
                total_loss_pnl += trade.pnl_percentage

            # Durchschnittliche Dauer des Trades berechnen (wenn Zeit vorhanden)
            if trade.entry_time and trade.exit_time:
                entry_time = datetime.fromisoformat(trade.entry_time)
                exit_time = datetime.fromisoformat(trade.exit_time)
                total_duration += (exit_time - entry_time).total_seconds()

        # Gewinnrate berechnen (falls Trades vorhanden sind)
        if result.no_of_trades > 0:
            result.winrate = (total_win_count / result.no_of_trades) * 100

        # Durchschnittliche Gewinne/Verluste berechnen
        result.average_win = (total_win_pnl / total_win_count) if total_win_count > 0 else 0.0
        result.average_loss = (total_loss_pnl / total_loss_count) if total_loss_count > 0 else 0.0

        # Risiko-Ertrags-Verhältnis berechnen
        if result.average_loss != 0:
            result.risk_ratio = abs(result.average_win / result.average_loss)
        else:
            result.risk_ratio = float('inf') if result.average_win > 0 else 0.0

            # Gesamt PnL und Max Drawdown
        result.pnl_percentage += total_pnl
        result.max_drawdown = max_drawdown if max_drawdown != float('-inf') else 0.0
        result.average_duration = (total_duration / result.no_of_trades) if result.no_of_trades > 0 else 0.0

        # Gewinn-, Verlust- und Break-even-Zahlen setzen
        result.win_count += total_win_count
        result.loss_count += total_loss_count
        result.break_even_count = result.no_of_trades - (total_win_count + total_loss_count)

        return result

    @staticmethod
    def _wait_for_threads(threads: list[threading.Thread]):
        while True:
            alive = False  # Assume all threads are dead
            for thread in threads:
                if thread.is_alive():
                    alive = True  # Found at least one active thread
                    break
            if not alive:  # If no threads are alive, exit the loop
                break

    def _fetch_test_assets(self):
        self._asset_selection = self._backtest_repository.find_assets_in_testdata()

    def _get_asset_classes(self, test_assets: list[str]) -> dict[str, str]:
        asset_classes: dict[str, str] = {}
        for asset in test_assets:
            asset_classes[asset] = self._backtest_repository.find_asset_class_name_by_asset(asset)
        return asset_classes

    def _prepare_test_data(self, test_assets: list[str]) -> dict[str, list[Candle]]:
        test_data: dict[str, list[Candle]] = {}

        for asset in test_assets:
            asset_candles: list[Candle] = self._backtest_repository.find_candles_by_asset(asset=asset)

            sorted_candles = sorted(asset_candles, key=lambda x: x.iso_time)

            test_data[asset] = sorted_candles

        return test_data
