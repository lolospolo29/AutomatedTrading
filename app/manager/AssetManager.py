import threading

from app.mappers.AssetMapper import AssetMapper
from app.models.asset.Asset import Asset
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.asset.SMTPair import SMTPair


class AssetManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AssetManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.assets: dict = {}
            self._AssetMapper = AssetMapper()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Register And Return Assets
    def registerAsset(self, asset: Asset) -> None:
        if not asset in self.assets:
            self.assets[asset.name] = asset
            print(f"Asset '{asset.name}' created and added to Asset Manager.")
        print(f"Asset '{asset.name}' already exists.")

    def returnAllAssets(self):
        assets = []
        for name,asset in self.assets.items():
            assets.append(name)
        return assets
    # endregion

    # region Add Functions
    def addCandle(self, json: dict) -> Candle:
        candle: Candle = self._AssetMapper.mapCandleFromTradingView(json)
        if candle.asset in self.assets:
            self.assets[candle.asset].addCandle(candle)
            return candle
        raise ValueError
    # endregion

    # region Return Functions
    def returnRelations(self, asset: str, broker: str) -> list[AssetBrokerStrategyRelation]:
        if asset in self.assets:
            return self.assets[asset].returnRelationsForBroker(broker)
        raise ValueError(f"Asset '{asset}' not found.")

    def returnSMTPair(self, asset: str) ->SMTPair:
        if asset in self.assets:
            return self.assets[asset].returnSMTPair()
        raise ValueError(f"Asset '{asset}' not found.")

    def returnBroker(self,asset: str, strategy: str):
        if asset in self.assets:
            return self.assets[asset].returnBrokers(strategy)
        raise ValueError(f"Asset '{asset}' not found.")

    def returnCandles(self, asset: str, broker: str, timeFrame: int) -> list[Candle]:
        if asset in self.assets:
            return self.assets[asset].returnCandles(timeFrame, broker)
        raise ValueError(f"Asset '{asset}' not found.")

    def returnAllRelations(self,asset: str):
        if asset in self.assets:
            return self.assets[asset].brokerStrategyAssignment
        raise ValueError(f"Asset '{asset}' not found.")
    # endregion



