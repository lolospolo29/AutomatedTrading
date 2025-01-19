import threading

from app.db.mongodb.mongoDBData import mongoDBData
from app.mappers.AssetMapper import AssetMapper
from app.models.asset.Asset import Asset
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.asset.SMTPair import SMTPair
from app.monitoring.logging.logging_startup import logger


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
        logger.info(f"Adding candle to db:{candle.asset}")
        try:
            if candle.timeframe >= 5:
                self._mongo_db_data.add_candle_to_db(candle.asset, candle)
        except Exception as e:
            logger.critical("Failed to add candle to db with exception {}".format(e))

    def received_candles(self, asset: str) -> Candle:
        pass
    # endregion

    # region Register And Return Assets
    def register_asset(self, asset: Asset) -> bool:
        logger.info(f"Register Asset to db:{asset}")

        if not asset in self.assets:
            self.assets[asset.name] = asset
            logger.info("Registered asset {}".format(asset.name))
            return True
        logger.warning("Asset {} already registered".format(asset.name))
        return False

    def return_all_assets(self):
        assets = []
        for name,asset in self.assets.items():
            assets.append(name)
        return assets
    # endregion

    # region Add Functions
    def add_candle(self, json: dict) -> Candle:
        try:
            candle: Candle = self._asset_mapper.map_candle_from_trading_view(json)
            logger.info(f"Add Candle to:{candle.asset}")

            if candle.asset in self.assets:
                self.assets[candle.asset].add_candle(candle)
                return candle
        except Exception as e:
            logger.exception("Failed to add candle to db with exception {}".format(e))
    # endregion

    # region Return Functions
    def return_relations(self, asset: str, broker: str) -> list[AssetBrokerStrategyRelation]:
        try:
            if asset in self.assets:
                logger.info(f"Return Relations for:{asset}")
                return self.assets[asset].return_relations_for_broker(broker)
        except Exception as e:
            logger.exception("Failed to return relations for asset {}".format(asset))

    def return_smt_pair(self, asset: str) ->SMTPair:
        try:
            if asset in self.assets:
                logger.info(f"Return SMT Pair for:{asset}")
                return self.assets[asset].return_smt_pair()
        except Exception as e:
            logger.exception("Failed to return SMTPair for asset {}".format(asset))

    def return_candles(self, asset: str, broker: str, timeFrame: int) -> list[Candle]:
        try:
            if asset in self.assets:
                logger.info(f"Return Candles for:{asset}")
                return self.assets[asset].return_candles(timeFrame, broker)
        except Exception as e:
            logger.exception("Failed to return candles for asset {}".format(asset))

    def return_all_relations(self, asset: str):
        try:
            if asset in self.assets:
                logger.info(f"Return All Relations for:{asset}")
                return self.assets[asset].relations
        except Exception as e:
            logger.exception("Failed to return relations for asset {}".format(asset))
    # endregion



