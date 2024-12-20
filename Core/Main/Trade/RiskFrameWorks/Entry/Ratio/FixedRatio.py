import inspect

from Core.Main.Trade.OrderDirectionEnum import OrderDirection
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.BaseRatio import BaseRatio
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Models.ProfitStopEntry import ProfitStopEntry
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Pattern.BasicRatioSort import BasicRatioSort
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Pattern.ModeRatioSort import ModeRatioSort
from Core.Main.Trade.RiskFrameWorks.RiskModeEnum import RiskMode


class FixedRatio(BaseRatio):

    # region Profit Stop Entry List Calculation
    def calculateStopsByEntryAndProfit(self, entry: list[float], profit: list[float], ratio: float, mode: str, direction: str)\
            -> list[ProfitStopEntry]:

        profit.sort()
        highestTp = profit[-1]  # Highest TP is the last in sorted order
        lowestTp = profit[0]  # Lowest TP is the first in sorted order

        if direction == "Buy":
            entry.sort()
            profit.sort()
        if direction == "Sell":
            entry.sort(reverse=True)
            profit.sort(reverse=True)

        profitStopEntryList = []

        for i in range(len(entry)):
            entryPrice = entry[i]

            tpLevel = self._returnHighestLevel(profit)
            stop = self.calculateStop(entryPrice, tpLevel, ratio)
            if len(profit) > 1:
                profit.remove(tpLevel)

            if direction == "Buy":
                    if not stop  < entryPrice < tpLevel:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = highestTp
                        if not stop  < entryPrice < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

            if direction == "Sell":
                    if not stop > entryPrice > tpLevel:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = lowestTp
                        if not stop > entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

        return profitStopEntryList

    def calculateProfitsByEntryAndStop(self, entry: list[float], stops: list[float], ratio: float, mode: RiskMode,
                                       direction: OrderDirection,modeRatioSort: ModeRatioSort)-> list[ProfitStopEntry]:
        return self._baseMethod(entry, stops, ratio, mode,direction, modeRatioSort,self.calculateProfit)

    def calculateEntriesByStopAndProfit(self, stop: list[float], profit: list[float], ratio: float, mode: str, direction: str)\
            -> list[ProfitStopEntry]:

        profit.sort()
        highestTp = profit[-1]  # Highest Stop is the last in sorted order
        lowestTp = profit[0]  # Lowest Stop is the first in sorted order

        if direction == "Buy":
            stop.sort()
            profit.sort()
        if direction == "Sell":
            stop.sort(reverse=True)
            profit.sort(reverse=True)

        profitStopEntryList = []

        for i in range(len(stop)):
            stopPrice = stop[i]

            if direction == "Buy":
                    tpLevel = self._returnHighestLevel(profit)
                    entry = self.calculateEntryPrice(stopPrice, tpLevel, ratio)
                    if len(profit) > 1:
                        profit.remove(tpLevel)

                    if not stopPrice < entry < tpLevel :
                        entry = self.calculateEntryPrice(stopPrice, highestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = highestTp
                        if not stopPrice < entry < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stopPrice, entry))

            if direction == "Sell":
                    tpLevel = self._returnLowestLevel(profit)
                    entry = self.calculateEntryPrice(stopPrice, tpLevel, ratio)
                    if len(profit) > 1:
                        profit.remove(tpLevel)

                    if not tpLevel < entry < stopPrice:
                        entry = self.calculateProfit(stopPrice, lowestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = lowestTp
                        if not tpLevel < entry < stopPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stopPrice, entry))

        return profitStopEntryList
    # endregion
    def _baseMethod(self, referenceList1: list[float], referenceList2: list[float], ratio: float, mode: RiskMode,
                                       direction: OrderDirection,modeRatioSort: ModeRatioSort,func):
        referenceList2.sort()

        if direction == OrderDirection.BUY:
            referenceList1.sort()
            referenceList2.sort()
        if direction == OrderDirection.SELL:
            referenceList1.sort(reverse=True)
            referenceList2.sort(reverse=True)

        profitStopEntryList = []

        for i in range(len(referenceList1)):
            ref = referenceList1[i]

            ref2 = modeRatioSort.sort(referenceList2,mode,direction)
            ref3 = func(ref, ref2, ratio)
            if len(referenceList2) > 1:
                referenceList2.remove(ref2)

            if not self.isConditionFullFilled(ref3,ref2,ref,direction):
                referenceList2.append(ref2)
                continue

            frame = inspect.currentframe()
            args, _, _, values = inspect.getargvalues(frame)
            param_name = [name for name in args if values[name] is referenceList1]
            if "entry" in param_name:
                print(f"Called with parameter name: {param_name[0]}, value: {param}")

            profitStopEntryList.append(ProfitStopEntry(ref3, ref2, ref))


        return profitStopEntryList

fx = FixedRatio()
fx.calculateProfitsByEntryAndStop([123,124,124,125,130],[125,126,128,129],2,RiskMode.AGGRESSIVE,OrderDirection.SELL,BasicRatioSort())