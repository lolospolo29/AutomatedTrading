from Models.Main.Asset.Asset import Asset
from Models.Main.Asset.Candle import Candle
from Services.DBService import DBService


class AssetManager:
    def __init__(self, dbService: DBService):
        self.assets: dict = {}
        self._DBService: DBService = dbService

    def registerAsset(self, asset: Asset) -> None:
        if not asset in self.assets:
            self.assets[asset.name] = asset
            print(f"Asset '{asset.name}' created and added to Asset Manager.")

    def addCandle(self, json: dict):
        mappedCandle: Candle = self._DBService.autoMapper(json)
        if mappedCandle.asset in self.assets:
            self.assets[mappedCandle.asset].addCandle(mappedCandle)
            return mappedCandle.asset, mappedCandle.broker, mappedCandle.timeFrame


    # def dailyDataArchive(self):
    #
    #     # Iterate over the assets
    #     for asset_name, asset in self.assets.items():
    #         timeFrames = self.returnAllCurrentTimeFrames(asset.name)
    #         for timeFrame in timeFrames:
    #             for assetData in asset.currentData:
    #                 if assetData.timeFrame == timeFrame:
    #                     currentData = assetData.toDict()
    #                     if len(assetData.open) != 0:
    #                         self._DBService.addDataToDB(asset.name, currentData)
    #                     break
    #
    #         self._DBService.returnRetrieveOrDoArchive(asset.name, "archive")
    #
    # def recentDataRetriever(self):
    #
    #     for asset_name, asset in self.assets.items():
    #         strategyDataList = self._DBService.returnRetrieveOrDoArchive(asset.name, "retrieve")
    #         for strategyData in strategyDataList:
    #             self.addPreviousData(asset.name, self._DBService.autoMapper(strategyData))
    #
    # def clearAllData(self):
    #     for asset_name, asset in self.assets.items():
    #         self.assets[asset.name].currentData = []
    #         # self.assets[asset.name].previousData = []
