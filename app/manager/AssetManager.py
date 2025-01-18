import threading

from app.db.mongodb.mongoDBData import mongoDBData
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
            self._mongo_db_data = mongoDBData()
            self._asset_mapper = AssetMapper()
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region CRUD

    def add_candle_to_db(self, candle: Candle):
        if candle.timeframe >= 5:
            self._mongo_db_data.add_candle_to_db(candle.asset, candle)

    def received_candles(self, asset: str) -> Candle:
        pass
    # endregion

    # region Register And Return Assets
    def register_asset(self, asset: Asset) -> bool:
        if not asset in self.assets:
            self.assets[asset.name] = asset
            print(f"Asset '{asset.name}' created and added to Asset Manager.")
            return True
        print(f"Asset '{asset.name}' already exists.")
        return False

    def return_all_assets(self):
        assets = []
        for name,asset in self.assets.items():
            assets.append(name)
        return assets
    # endregion

    # region Add Functions
    def add_candle(self, json: dict) -> Candle:
        candle: Candle = self._asset_mapper.map_candle_from_trading_view(json)
        if candle.asset in self.assets:
            self.assets[candle.asset].add_candle(candle)
            return candle
        raise ValueError
    # endregion

    # region Return Functions
    def return_relations(self, asset: str, broker: str) -> list[AssetBrokerStrategyRelation]:
        if asset in self.assets:
            return self.assets[asset].return_relations_for_broker(broker)
        raise ValueError(f"Asset '{asset}' not found.")

    def return_smt_pair(self, asset: str) ->SMTPair:
        if asset in self.assets:
            return self.assets[asset].return_smt_pair()
        raise ValueError(f"Asset '{asset}' not found.")

    def return_candles(self, asset: str, broker: str, timeFrame: int) -> list[Candle]:
        if asset in self.assets:
            return self.assets[asset].return_candles(timeFrame, broker)
        raise ValueError(f"Asset '{asset}' not found.")

    def return_all_relations(self, asset: str):
        if asset in self.assets:
            return self.assets[asset].relations
        raise ValueError(f"Asset '{asset}' not found.")
    # endregion



