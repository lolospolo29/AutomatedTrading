from typing import Any

from Models.Main.Asset.Asset import Asset
from Models.Main.Asset.Candle import Candle
from Models.Main.Asset.CandleSeries import CandleSeries
from Services.DBService import DBService


class AssetManager:
    def __init__(self, dbService: DBService):
        self.assets: dict = {}
        self._DBService: DBService = dbService

    def registerAsset(self, asset: Asset) -> None:
        if not asset in self.assets:
            self.assets[asset.name] = asset
            print(f"Asset '{asset.name}' created and added to Asset Manager.")

    def addCandle(self, json: dict) -> Any:
        mappedCandle: Candle = self._DBService.autoMapper(json)
        if mappedCandle.asset in self.assets:
            self.assets[mappedCandle.asset].addCandle(mappedCandle)
            return mappedCandle.asset, mappedCandle.broker, mappedCandle.timeFrame

    def returnCandles(self, asset: str, broker: str, timeFrame: int) -> list:
        if asset in self.assets:
            return self.assets[asset].returnCandles(timeFrame, broker)

    def returnRelations(self, asset: str, broker: str) -> list:
        if asset in self.assets:
            return self.assets[asset].returnRelationsForBroker(broker)

    def returnSMTPair(self, asset: str):
        if asset in self.assets:
            return self.assets[asset].returnSMTPair()

    def returnBroker(self,asset: str, strategy: str):
        if asset in self.assets:
            return self.assets[asset].returnBrokers(strategy)

    def returnAllRelations(self,asset: str):
        if asset in self.assets:
            return self.assets[asset].brokerStrategyAssignment

    def returnAllAssets(self):
        assets = []
        for name,asset in self.assets.items():
            assets.append(name)
        return assets

    def dailyDataArchive(self):
        # Iterate over the assets
        for name, asset in self.assets.items():
            candleSeries: list[CandleSeries] = self.assets[name].returnAllCandleSeries()
            for candleSerie in candleSeries:
                for candle in candleSerie.candleSeries:
                        self._DBService.addDataToDB(asset.name, candle.toDict())

            self._DBService.archiveData(asset.name)

    def recentDataRetriever(self, asset:str,broker: str, timeFrame:int,lookback: int) -> list:
        dbCandles = self._DBService.receiveData(asset, broker, timeFrame, lookback)
        candles = []
        if len(dbCandles) <= 0:
            return candles
        for candle in dbCandles:
            candles.append(self._DBService.autoMapper(candle))
        return candles


