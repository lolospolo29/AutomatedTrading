import threading
import uuid

from app.db.mongodb.BacktestRepository import BacktestRepository
from app.helper.factories.StrategyFactory import StrategyFactory
from app.models.asset.Candle import Candle
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

    def __init__(self,backtest_repository:BacktestRepository):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.__factory = StrategyFactory()
            self._backtest_repository = backtest_repository
            self._initialized = True  # Markiere als initialisiert

    def start_backtesting_strategy(self,strategy:str,test_assets:list[str])->Result:

        test_data:dict[str,list[Candle]] = self._prepare_test_data(test_assets)

        strategy = self.__factory.return_strategy(strategy)

        result = Result(strategy=strategy.name,result_id=str(uuid.uuid4()),equity_curve=[])

        modules:list[TestModule] = []

        threads = []

        if strategy is None:
            logger.error(f"Strategy {strategy} not found in Backtest Service")
            return result

        for asset in test_assets:
            logger.info(f"Starting backtest for {asset}")

            module = TestModule(strategy.model_copy()
                                      ,test_data[asset], strategy.timeframes,result.result_id)
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

    def get_test_results(self,strategy:str=None)->Result:
        pass

    def add_test_data(self,candles:list[Candle]):
        for candle in candles:
            self._backtest_repository.add_candle(candle.asset,candle)

    @staticmethod
    def _add_module_statistic_to_result(module:TestModule, result:Result)->Result:
        pass

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

    def _prepare_test_data(self, test_assets: list[str]) -> dict[str, list[Candle]]:
        test_data: dict[str, list[Candle]] = {}

        for asset in test_assets:
            asset_candles: list[Candle] = self._backtest_repository.find_candles_by_asset(asset=asset)

            sorted_candles = sorted(asset_candles, key=lambda x: x.iso_time)

            test_data[asset] = sorted_candles

        return test_data
