import time
from typing import Any, Dict

from Core.Main.Asset.SubModels.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Config.GlobalStatements import getLockState, setLockState
from Monitoring.TimeWrapper import logTime
from Services.Manager.AssetManager import AssetManager
from Services.Manager.StrategyManager import StrategyManager
from Services.Manager.TradeManager import TradeManager


class TradingService:
    def __init__(self, assetManager: AssetManager, tradeManager: TradeManager, strategyManager: StrategyManager):
        self._AssetManager: AssetManager = assetManager
        self._TradeManager: TradeManager = tradeManager
        self._StrategyManager: StrategyManager = strategyManager

    @logTime
    def handlePriceActionSignal(self, jsonData: Dict[str, Any]) -> None:

        while getLockState():
            time.sleep(1)

        asset, broker, timeFrame = self._AssetManager.addCandle(jsonData)
        candles : list = self._AssetManager.returnCandles(asset, broker, timeFrame)
        self.analyzeStrategy(asset, broker, timeFrame, candles)

    @logTime
    def analyzeStrategy(self, asset: str, broker: str, timeFrame:int,candles:list) -> None:

        relations: list = self._AssetManager.returnRelations(asset, broker)

        for relation in relations:
            self._StrategyManager.analyzeStrategy(candles, relation, timeFrame)

            _ids = [candle.id for candle in candles]
            self._StrategyManager.updateFrameWorkHandler(_ids, relation, timeFrame)

            self._StrategyManager.getEntry(candles, relation, timeFrame)

    def executeDailyTasks(self) -> None:
        """ Aufgaben, die täglich um 04:00 UTC (00:00 NY) ausgeführt werden """
        if not getLockState():  # Nur wenn der Lock nicht aktiv ist

            setLockState(True)
            print("Daily tasks execution started at 04:00 UTC.")

            self.dailyArchive()

            # Dies wird nur einmal um 04:00 Uhr ausgeführt
            assets = self._AssetManager.returnAllAssets()
            for asset in assets:
                relations: list[AssetBrokerStrategyRelation] = self._AssetManager.returnAllRelations(asset)

                for relation in relations:
                    expectedTimeFrames: list = self._StrategyManager.returnExpectedTimeFrame(relation.strategy)
                    dataDuration: int = self._StrategyManager.returnDuration(relation.strategy)
                    for expectedTimeFrame in expectedTimeFrames:
                        candles: list = self._AssetManager.recentDataRetriever(relation.asset,
                                                                               relation.broker,expectedTimeFrame.timeFrame
                                                                               , dataDuration)
                        self.analyzeStrategy(asset, relation.broker, expectedTimeFrame.timeFrame, candles)

            setLockState(False)

    def dailyArchive(self) -> None:
        self._AssetManager.dailyDataArchive()
        self._TradeManager.archiveTrades()
