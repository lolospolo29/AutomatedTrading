import time
from typing import Any, Dict

from Services.Manager.AssetManager import AssetManager
from Services.Manager.StrategyManager import StrategyManager
from Services.Manager.TradeManager import TradeManager


class TradingService:
    def __init__(self, assetManager: AssetManager, tradeManager: TradeManager, strategyManager: StrategyManager):
        self._AssetManager: AssetManager = assetManager
        self._TradeManager: TradeManager = tradeManager
        self._StrategyManager: StrategyManager = strategyManager
        self.lockActive: bool = False  # Flag um den Status des Locks zu verfolgen

    def handlePriceActionSignal(self, jsonData: Dict[str, Any]) -> None:

        while self.lockActive:
            time.sleep(1)
        asset, broker, timeFrame = self._AssetManager.addCandle(jsonData)
        self.analyzeStrategy(asset, broker, timeFrame)

    def analyzeStrategy(self, asset: str, broker: str, timeFrame:int) -> None:
        candles : list = self._AssetManager.returnCandles(asset, broker, timeFrame)

        relations: list = self._AssetManager.returnRelations(asset, broker)

        self._StrategyManager.analyzeStrategy(candles, relations, timeFrame)


    # def executeDailyTasks(self) -> None:
    #     """ Aufgaben, die täglich um 04:00 UTC (00:00 NY) ausgeführt werden """
    #     if not self.lockActive:  # Nur wenn der Lock nicht aktiv ist
    #         self.lockActive = True  # Lock aktivieren
    #         print("Daily tasks execution started at 04:00 UTC.")
    #
    #         # Dies wird nur einmal um 04:00 Uhr ausgeführt
    #
    #         self.dailyArchive()
    #
    #         self.dailyClearer()
    #
    #         self.RecentRetriever()
    #
    #         self.lockActive = False  # Lock wieder deaktivieren nach der Ausführung
    #
    # def dailyArchive(self) -> None:
    #     self._AssetManager.dailyDataArchive()
    #     self._TradeManager.archiveClosedTrades()
    #
    # def dailyClearer(self) -> None:
    #     self._AssetManager.clearAllData()
    #     self._TradeManager.clearOpenTrades()
    #
    # def RecentRetriever(self) -> None:
    #     self._AssetManager.recentDataRetriever()
    #     self._TradeManager.findOpenTrades()
