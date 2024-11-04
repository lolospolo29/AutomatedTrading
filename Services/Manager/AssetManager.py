class AssetManager:
    def __init__(self, DBService):
        self.assets: dict = {}
        self._DBService = DBService

    def registerAsset(self, asset):
        self.assets[asset.name] = asset
        print(f"Asset '{asset.name}' created and added to Asset Manager.")

    def addPreviousData(self, asset_name, strategyData):
        if asset_name in self.assets:
            self.assets[asset_name].addPreviousData(strategyData)

    def addCurrentData(self, tradingData):
        """
        Add a new timeframe to a specific asset.
        """
        tradingData = self._DBService.autoMapper(tradingData)
        if tradingData.asset in self.assets:
            self.assets[tradingData.asset].addCurrentData(tradingData)
        return tradingData.asset

    def returnStrategyName(self, assetName):
        if assetName in self.assets:
            return self.assets[assetName].strategyName

    def returnAllCurrentTimeFrames(self, assetName):
        if assetName in self.assets:
            return self.assets[assetName].returnAllCurrentTimeFrames()

    def returnCurrentDataByTimeFrame(self, assetName, timeFrame):
        data = []
        if assetName in self.assets:
            data.append(self.assets[assetName].returnCurrentDataByTimeFrameAndDataPoints(timeFrame, 60))
        return data

    def returnCurrentDataByIds(self, assetName, _ids):
        data = []
        if assetName in self.assets:
            data.append(self.assets[assetName].returnCurrentDataByIds(_ids))
        return data

    def returnPreviousDataByIds(self, assetName, _ids):
        data = []
        if assetName in self.assets:
            data.append(self.assets[assetName].returnPreviousDataByIds(_ids))
        return data

    def dailyDataArchive(self):

        # Iterate over the assets
        for asset_name, asset in self.assets.items():
            timeFrames = self.returnAllCurrentTimeFrames(asset.name)
            for timeFrame in timeFrames:
                for assetData in asset.currentData:
                    if assetData.timeFrame == timeFrame:
                        currentData = assetData.toDict()
                        if len(assetData.open) != 0:
                            self._DBService.addDataToDB(asset.name, currentData)
                        break

            self._DBService.returnRetrieveOrDoArchive(asset.name, "archive")

    def recentDataRetriever(self):

        for asset_name, asset in self.assets.items():
            strategyDataList = self._DBService.returnRetrieveOrDoArchive(asset.name, "retrieve")
            for strategyData in strategyDataList:
                self.addPreviousData(asset.name, self._DBService.autoMapper(strategyData))

    def clearAllData(self):
        for asset_name, asset in self.assets.items():
            self.assets[asset.name].currentData = []
            self.assets[asset.name].previousData = []
