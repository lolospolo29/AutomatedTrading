from typing import Any

from Core.Main.Trade.RiskFrameWorks.Ratio.BaseRatio import BaseRatio
from Core.Main.Trade.RiskFrameWorks.Ratio.FixedRatio import FixedRatio
from Core.Main.Trade.RiskFrameWorks.Ratio.Models.ProfitStopEntry import ProfitStopEntry


class RangeRatio(BaseRatio):

    def calculateProfitByEntryAndStopWithRangeMatrix(self, entry: float, stop: float, rangeRatio: list[int]
                                                     , mode: str) -> float:
        estimatedProfits = []
        for ratio in rangeRatio:
            profit = self.calculateProfit(entry, stop, ratio)
            if self._isConditionFullFilled(entry, stop, profit):
                estimatedProfits.append(profit)

        estimatedProfits.sort()

        return self._returnElementBasedOnMode(estimatedProfits, mode)

    def calculateStopByEntryAndProfitWithRangeMatrix(self, entry: float, profit: float,
                                                     rangeRatio: list[int], mode: str) -> float:
        estimatedStops = []
        for ratio in rangeRatio:
            stop = self.calculateStop(entry, profit, ratio)
            if self._isConditionFullFilled(entry, stop, profit):
                estimatedStops.append(stop)

        estimatedStops.sort()

        return self._returnElementBasedOnMode(estimatedStops, mode)

    def calculateEntryByStopAndProfitWithRangeMatrix(self,stop: float,profit: float,
                                                     rangeRatio: list[int], mode: str) -> float:
        estimatedEntries = []
        for ratio in rangeRatio:
            entry = self.calculateEntryPrice(stop, profit, ratio)
            if self._isConditionFullFilled(entry,stop,profit):
                estimatedEntries.append(stop)

        estimatedEntries.sort()

        return self._returnElementBasedOnMode(estimatedEntries, mode)

    def calculateProfitsByEntryAndStopWithRangeMatrix(self, entry: list[float], stop: list[float],rangeRatio:
    list[int], mode: str,direction: str) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []
        fxr = FixedRatio()

        for r in rangeRatio:
            profitsWithFixedRatio = fxr.calculateProfitsByEntryAndStop(entry, stop, r, mode,direction)
            profitStopEntryList.extend(profitsWithFixedRatio)

        adjustedStopEntryList = []

        if len(profitStopEntryList) > 0:
            for e in entry:
                eProfits = [p for p in profitStopEntryList if p.profit == e]
                eProfits.sort(key=lambda x: x.profit)
                adjustedStopEntryList.append(self._returnElementBasedOnMode(eProfits, mode))

        return profitStopEntryList

    @staticmethod
    def _isConditionFullFilled(entry: float, stop: float, profit: float) -> bool:
        if stop < entry < profit:
            return True
        if stop > entry > profit:
            return True
        return False

    @staticmethod
    def _returnElementBasedOnMode(referencePrices:list[Any], mode: str) -> Any:
        if not len(referencePrices) > 0:
            raise ValueError

        if mode == "aggressive":
            return referencePrices[-1]
        if mode == "moderat":
            if len(referencePrices) == 1:  # Only one TP level
                return referencePrices[0]
            elif len(referencePrices) == 2:  # Two TP levels
                return referencePrices[1]
            else:  # Three or more TP levels
                return referencePrices[3 * len(referencePrices) // 4]  # Third quartile
        if mode == "safe":
            return referencePrices[0]
