from typing import Any

from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.BaseRatio import BaseRatio
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.FixedRatio import FixedRatio
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Models.ProfitStopEntry import ProfitStopEntry


class RangeRatio(BaseRatio):

    def __init__(self):
        self.fixedRatio = FixedRatio()

    # region Calculate Profit Stop Entry With Matrix Calculation
    def calculateProfitByEntryAndStopWithRangeMatrix(self, entry: float, stop: float, rangeRatio: list[int]
                                                     , mode: str,direction: str) -> float:
        estimatedProfits = []
        for ratio in rangeRatio:
            profit = self.calculateProfit(entry, stop, ratio)
            if self._isConditionFullFilled(entry, stop, profit):
                estimatedProfits.append(profit)

        if direction == "Buy":
            estimatedProfits.sort(reverse=True)
        if direction == "Sell":
            estimatedProfits.sort()

        return self._returnElementBasedOnMode(estimatedProfits, mode)

    def calculateStopByEntryAndProfitWithRangeMatrix(self, entry: float, profit: float,
                                                     rangeRatio: list[int], mode: str,direction: str) -> float:
        estimatedStops = []
        for ratio in rangeRatio:
            stop = self.calculateStop(entry, profit, ratio)
            if self._isConditionFullFilled(entry, stop, profit):
                estimatedStops.append(stop)

        if direction == "Buy":
            estimatedStops.sort()
        if direction == "Sell":
            estimatedStops.sort(reverse=True)

        return self._returnElementBasedOnMode(estimatedStops, mode)

    def calculateEntryByStopAndProfitWithRangeMatrix(self,stop: float,profit: float,
                                                     rangeRatio: list[int], mode: str,direction: str) -> float:
        estimatedEntries = []
        for ratio in rangeRatio:
            entry = self.calculateEntryPrice(stop, profit, ratio)
            if self._isConditionFullFilled(entry,stop,profit):
                estimatedEntries.append(entry)

        if direction == "Buy":
            estimatedEntries.sort()
        if direction == "Sell":
            estimatedEntries.sort(reverse=True)

        return self._returnElementBasedOnMode(estimatedEntries, mode)
    # endregion

    # region Calculate Profit Stop Entry With Matrix List Calculation
    def calculateProfitsByEntryAndStopWithRangeMatrix(self, entry: list[float], stop: list[float],rangeRatio:
    list[int], mode: str,direction: str) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for ratio in rangeRatio:
            profitsWithFixedRatio = self.fixedRatio.calculateProfitsByEntryAndStop(entry.copy(), stop.copy(), ratio, mode,direction)
            profitStopEntryList.extend(profitsWithFixedRatio)

        adjustedStopEntryList = []

        if len(profitStopEntryList) > 0:
            for e in entry:
                eProfits = [p for p in profitStopEntryList if p.entry == e]
                if direction == "Buy":
                    eProfits.sort(key=lambda x: x.profit, reverse=True)
                if direction == "Sell":
                    eProfits.sort(key=lambda x: x.profit)
                adjustedStopEntryList.append(self._returnElementBasedOnMode(eProfits, mode))

        return adjustedStopEntryList

    def calculateStopsByEntryAndProfitWithRangeMatrix(self, entry: list[float], profit: list[float], rangeRatio:
    list[int], mode: str, direction: str) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for ratio in rangeRatio:
            profitsWithFixedRatio = self.fixedRatio.calculateStopsByEntryAndProfit(entry.copy(), profit.copy(), ratio, mode, direction)
            profitStopEntryList.extend(profitsWithFixedRatio)

        adjustedStopEntryList = []

        if len(profitStopEntryList) > 0:
            for e in entry:
                eProfits = [p for p in profitStopEntryList if p.entry == e]
                if direction == "Buy":
                    eProfits.sort(key=lambda x: x.stop)
                if direction == "Sell":
                    eProfits.sort(key=lambda x: x.stop,reverse=True)
                adjustedStopEntryList.append(self._returnElementBasedOnMode(eProfits, mode))

        return adjustedStopEntryList

    def calculateEntriesByStopAndProfitWithRangeMatrix(self, stop: list[float], profit: list[float], rangeRatio:
    list[int], mode: str, direction: str) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for ratio in rangeRatio:
            profitsWithFixedRatio = self.fixedRatio.calculateEntriesByStopAndProfit(stop.copy(), profit.copy(), ratio, mode, direction)
            profitStopEntryList.extend(profitsWithFixedRatio)

        adjustedStopEntryList = []

        if len(profitStopEntryList) > 0:
            for s in stop:
                eProfits = [p for p in profitStopEntryList if p.stop == s]
                if direction == "Buy":
                    eProfits.sort(key=lambda x: x.entry)
                if direction == "Sell":
                    eProfits.sort(key=lambda x: x.entry,reverse=True)
                adjustedStopEntryList.append(self._returnElementBasedOnMode(eProfits, mode))

        return adjustedStopEntryList
    # endregion
