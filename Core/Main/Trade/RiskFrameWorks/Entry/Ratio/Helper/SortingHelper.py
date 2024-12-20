from typing import Any

from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Models.ProfitStopEntry import ProfitStopEntry


class SortingHelper:
    # region Filter Highest Lowest Element
    @staticmethod
    def returnHighestLevel(referencePriceList:list[float]):
        refHigh = 0
        for j in range(len(referencePriceList)):
            if referencePriceList[j] > refHigh:
                refHigh = referencePriceList[j]

        return refHigh

    @staticmethod
    def returnLowestLevel(referencePriceList:list[float]) -> float:
        refLow = 0
        for j in range(len(referencePriceList)):
            if j == 0:
                refLow = referencePriceList[j]
            if referencePriceList[j] < refLow:
                refLow = referencePriceList[j]

        return refLow
    # endregion

    # region Filter Quartile Element
    @staticmethod
    def returnThirdQuartileElementOrFirstOrSecond(referencePriceList:list) -> Any:
        if len(referencePriceList) == 1:  # Only one TP level
            return referencePriceList[0]
        elif len(referencePriceList) == 2:  # Two TP levels
            return referencePriceList[1]
        else:  # Three or more TP levels
            return referencePriceList[3 * len(referencePriceList) // 4]  # Third quartile

    @staticmethod
    def returnFirstQuartileElementOrFirstOrSecond(referencePriceList:list) -> Any:
        if len(referencePriceList) == 1:  # Only one TP level
            return referencePriceList[0]
        elif len(referencePriceList) == 2:  # Two TP levels
            return referencePriceList[0]
        else:  # Three or more TP levels
            return referencePriceList[len(referencePriceList) // 4]  # First quartile
    # endregion


    @staticmethod
    def reduceProfitStopEntryListByLimit(profitStopEntryList: list[ProfitStopEntry],mode: str,
                                         limit: int) -> list[ProfitStopEntry]:
        if len(profitStopEntryList) < limit:
            return profitStopEntryList

        # To-Do

        elementsToCut = limit - len(profitStopEntryList)
        midPoint = len(profitStopEntryList) // 2

        left = profitStopEntryList[:midPoint]
        right = profitStopEntryList[midPoint:]

        if mode == "aggressive":
            pass
