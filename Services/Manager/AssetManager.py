from Models.Asset.Asset import Asset


class AssetManager:
    def __init__(self, DBService):
        self.assets: dict = {}
        self._DBService = DBService

    def registerAsset(self, asset: Asset) -> None:
        self.assets[asset.name] = asset
        print(f"Asset '{asset.name}' created and added to Asset Manager.")

    def addStrategy(self, asset: str,strategy: str) -> None:
        if asset in self.assets:
            self.assets[asset].addStrategy(strategy)

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
