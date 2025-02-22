import threading
import uuid

from app.db.mongodb.AssetRepository import AssetRepository
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

    def __init__(self,asset_repository:AssetRepository):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.__factory = StrategyFactory()
            self._asset_repository = asset_repository
            self._initialized = True  # Markiere als initialisiert

    def _prepare_test_data(self,test_assets:list[str])->dict[str,list[Candle]]:
        test_data: dict[str, list[Candle]] = {}

        for asset in test_assets:
            asset_candles:list[Candle] = self._asset_repository.find_candles_by_asset(asset=asset)

            sorted_candles = sorted(asset_candles, key=lambda x: x.iso_time)

            test_data[asset] = sorted_candles

        return test_data

    def start_backtesting_strategy(self,strategy:str,test_assets:list[str]):

        test_data:dict[str,list[Candle]] = self._prepare_test_data(test_assets)

        strategy = self.__factory.return_strategy(strategy)

        result = Result(strategy=strategy.name,result_id=str(uuid.uuid4()))

        modules:list[TestModule] = []

        threads = []

        for asset in test_assets:
            if strategy is None:
                logger.error(f"Strategy {strategy} not found")
                raise Exception("Strategy not found")
            module = TestModule(strategy.model_copy()
                                      ,test_data[asset], strategy.timeframes,result.result_id)
            modules.append(module)
            thread = threading.Thread(target=module.start_module())
            threads.append(thread)
            thread.start()

        alive = False
        while not alive:
            for thread in threads:
                if thread.is_alive():
                    alive = True
                    break

    def get_test_results(self,strategy:str=None,asset:str=None):
        with self._lock:
            pass

    def add_test_data(self,candles:list[Candle]):
        for candle in candles:
            self._asset_repository.add_candle(candle.asset,candle)
