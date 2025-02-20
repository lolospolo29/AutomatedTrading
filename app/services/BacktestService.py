from app.db.mongodb.AssetRepository import AssetRepository
from app.helper.factories.StrategyFactory import StrategyFactory
from app.models.asset.Candle import Candle


class BacktestService:
    def __init__(self):
        self.__factory = StrategyFactory()
        self._asset_repository = AssetRepository()

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

