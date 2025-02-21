import threading

from app.db.mongodb.AssetRepository import AssetRepository
from app.helper.factories.StrategyFactory import StrategyFactory
from app.models.asset.Candle import Candle


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


    def get_test_results(self,strategy:str=None):
        pass

    def add_test_data(self):
        pass

    def start_backtesting(self,strategy:str,test_assets:list[str]):

        test_data:dict[str,list[Candle]] = {}

        for asset in test_assets:

            strategy = self.__factory.return_strategy(strategy)

            expected_time = strategy.timeframes

            candles = test_data[asset]

            for candle in candles:
                pass

