import threading
import uuid
from datetime import datetime
from logging import Logger

from files.db.repositories.BacktestRepository import BacktestRepository
from files.helper.builder.StrategyBuilder import StrategyBuilder
from files.models.asset.AssetClass import AssetClass
from files.models.asset.Candle import Candle
from files.models.backtest.BacktestInput import BacktestInput
from files.models.backtest.Result import Result
from files.models.backtest.TestModule import TestModule
from files.models.backtest.TradeResult import TradeResult


class BacktestService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(BacktestService, cls).__new__(cls)
        return cls._instance

    def __init__(self, backtest_repository: BacktestRepository,strategy_factory: StrategyBuilder
                 ,logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._builder = strategy_factory
            self._backtest_repository = backtest_repository
            self.logger = logger

            self._initialized = True  # Markiere als initialisiert

    def add_test_data(self, candles: list[Candle]):
        for candle in candles:
            self._backtest_repository.add_candle(candle)

    def start_backtesting_strategy(self, backtest_input: BacktestInput):

        test_data: dict[str, list[Candle]] = self._prepare_test_data(backtest_input.test_assets)

        asset_classes: dict[str, AssetClass] = self._get_asset_classes(backtest_input.test_assets)

        modules: list[TestModule] = []

        threads = []

        for asset in backtest_input.test_assets:
            strategy = (self._builder.create_strategy(backtest_input.strategy.name)
                        .add_entry(backtest_input.strategy.entry_strategy_id)
                        .add_exit(backtest_input.strategy.exit_strategy_id).build())

            if strategy is None:
                continue

            self.logger.info(f"Starting Backtest: {strategy.name} with Asset {asset}")

            module = TestModule(asset_class=asset_classes[asset], strategy=strategy, asset=asset
                                , candles=test_data[asset], trade_limit=backtest_input.trade_limit,logger=self.logger)
            modules.append(module)
            thread = threading.Thread(target=module.start_module)
            threads.append(thread)
            thread.start()

        self._wait_for_threads(threads)

        results = []

        for module in modules:
            result = self._create_result(module)
            results.append(result)

        for result in results:
            if result.no_of_trades > 0:
                self.logger.info(f"Writing Result to DB...,ResultId: {result.result_id}")
                self._backtest_repository.add_result(result)

    def get_asset_selection(self) -> list[str]:
        assets_dict =  self._backtest_repository.get_asset_selection()
        return [doc['asset'] for doc in assets_dict]

    def get_test_results(self, strategy: str = None) -> list[Result]:
        if strategy:
            return self._backtest_repository.find_result_by_strategy(strategy)
        else:
            return self._backtest_repository.find_results()

    def _create_result(self,module: TestModule) -> Result:
        """Fügt die Statistiken eines TestModules zum übergeordneten Result hinzu."""
        total_pnl = 0.0
        total_win_pnl = 0.0
        total_loss_pnl = 0.0
        total_win_count = 0
        total_loss_count = 0
        total_duration = 0.0
        total_break_even = 0.0
        total_risk_ratio = 0.0
        total_activated = 0
        max_drawdown = float('inf')

        result = Result(result_id=str(self._generate_custom_id(strategy_name=module.strategy.name, asset=module.asset)), strategy=module.strategy.name, asset=module.asset)

        # Alle TradeResults aus dem TestModule iterieren
        for trade in module.trade_results.values():
            trade: TradeResult = trade
            # Anzahl der Trades erhöhen
            result.no_of_trades += 1

            # Gewinn/Verlust berechnen
            total_pnl += trade.pnl_percentage
            max_drawdown = min(max_drawdown, trade.max_drawdown)  # Niedrigster Wert

            if trade.take_profit and trade.stop and trade.entry_price:
                distance_to_profit = trade.take_profit - trade.entry_price
                distance_to_stop = trade.stop - trade.entry_price
                risk_ratio = distance_to_profit / distance_to_stop
                total_risk_ratio += abs(risk_ratio)
                total_activated += 1

            if trade.pnl_percentage > 0:
                total_win_count += 1
                total_win_pnl += trade.pnl_percentage
            if trade.pnl_percentage < 0:
                total_loss_count += 1
                total_loss_pnl += trade.pnl_percentage
            if trade.pnl_percentage == 0:
                total_break_even += 1

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
        result.risk_ratio = total_risk_ratio / total_activated if total_activated > 0 else 0.0

            # Gesamt PnL und Max Drawdown
        result.pnl_percentage += total_pnl
        result.max_drawdown = max_drawdown if max_drawdown != float('-inf') else 0.0
        result.average_duration = (total_duration / result.no_of_trades) if result.no_of_trades > 0 else 0.0

        # Gewinn-, Verlust- und Break-even-Zahlen setzen
        result.win_count += total_win_count
        result.loss_count += total_loss_count
        result.break_even_count += total_break_even

        return result

    @staticmethod
    def _generate_custom_id(strategy_name, asset):
        now = datetime.utcnow()
        timestamp = now.strftime("%H%M%S%d%m%Y")  # Format: HHMMSSDDMMYYYY
        short_uuid = str(uuid.uuid4().hex)[:4]  # Take first 4 chars from UUID

        # Shorten strategy and asset names (max 3 chars each to fit in 16)
        strategy_part = strategy_name[:3].upper()
        asset_part = asset[:3].upper()

        # Construct the 16-character ID
        custom_id = f"{timestamp[:8]}{short_uuid}{strategy_part}{asset_part}"

        return custom_id[:16]  # Ensure it remains 16 chars

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

    def _get_asset_classes(self, test_assets: list[str]) -> dict[str, AssetClass]:
        asset_classes: dict[str, AssetClass] = {}
        for asset in test_assets:
            asset:str
            asset_classes[asset] = self._backtest_repository.find_asset_class_by_id(asset)
        return asset_classes

    def _prepare_test_data(self, test_assets: list[str]) -> dict[str, list[Candle]]:
        test_data: dict[str, list[Candle]] = {}

        for asset in test_assets:
            asset_candles: list[Candle] = self._backtest_repository.find_candles_by_asset(asset=asset)

            sorted_candles = sorted(asset_candles, key=lambda x: x.iso_time)

            test_data[asset] = sorted_candles

        return test_data
