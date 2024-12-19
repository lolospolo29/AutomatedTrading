from Core.Main.Trade.RiskFrameWorks.Ratio.BaseRatio import BaseRatio
from Core.Main.Trade.RiskFrameWorks.Ratio.Models.ProfitStopEntry import ProfitStopEntry


class FixedRatio(BaseRatio):

    def calculateStopsByEntryAndProfit(self, entry: list[float], profit: list[float], ratio: float, mode, direction)\
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

            if mode == "aggressive":
                if direction == "Buy":
                    tpLevel = self._returnHighestLevel(profit)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    if len(profit) > 1:
                        profit.remove(tpLevel)

                    if not stop  < entryPrice < tpLevel:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = highestTp
                        if not stop  < entryPrice < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = self._returnLowestLevel(profit)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    if len(profit) > 1:
                        profit.remove(tpLevel)

                    if not stop > entryPrice > tpLevel:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = lowestTp
                        if not stop > entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

            if mode == "moderat":
                if direction == "Buy":
                    tpLevel = 0
                    if len(profit) == 1:  # Only one TP level
                        tpLevel = profit[0]
                    elif len(profit) == 2:  # Two TP levels
                        tpLevel = profit[1]
                    else:  # Three or more TP levels
                        tpLevel = profit[3 * len(profit) // 4]  # Third quartile
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)

                    if len(profit) > 1:
                        profit.remove(tpLevel)
                    if not stop < entryPrice < tpLevel:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = highestTp
                        if not stop < entryPrice < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = 0
                    # Handle midpoints
                    if len(profit) == 1:  # Only one TP level
                        tpLevel = profit[0]
                    elif len(profit) == 2:  # Two TP levels
                        tpLevel = profit[0]
                    else:  # Three or more TP levels
                        tpLevel = profit[len(profit) // 4]  # First quartile

                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    if len(profit) > 1:
                        profit.remove(tpLevel)
                    if not stop > entryPrice > tpLevel:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = lowestTp
                        if not stop > entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

            if mode == "safe":
                if direction == "Buy":
                    tpLevel = self._returnLowestLevel(profit)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    if len(profit) > 1:
                        profit.remove(tpLevel)

                    if not stop < entryPrice < tpLevel:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = highestTp
                        if not stop < entryPrice < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = self._returnHighestLevel(profit)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    if len(profit) > 1:
                        profit.remove(tpLevel)

                    if not stop > entryPrice > tpLevel:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = lowestTp
                        if not stop > entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

        return profitStopEntryList

    def calculateProfitsByEntryAndStop(self, entry: list[float], stops: list[float], ratio: float, mode, direction)\
            -> list[ProfitStopEntry]:

        stops.sort()
        highestStop = stops[-1]  # Highest Stop is the last in sorted order
        lowestStop = stops[0]  # Lowest Stop is the first in sorted order

        if direction == "Buy":
            entry.sort()
            stops.sort()
        if direction == "Sell":
            entry.sort(reverse=True)
            stops.sort(reverse=True)

        profitStopEntryList = []

        for i in range(len(entry)):
            entryPrice = entry[i]

            if mode == "aggressive":
                if direction == "Buy":
                    stopLevel = self._returnLowestLevel(stops)
                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)
                    if len(stops) > 1:
                        stops.remove(stopLevel)

                    if not stopLevel < entryPrice < profit :
                        profit = self.calculateProfit(entryPrice, lowestStop, ratio)
                        stops.append(stopLevel)
                        stopLevel = lowestStop
                        if not stopLevel < entryPrice < profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stopLevel, entryPrice))

                if direction == "Sell":
                    stopLevel = self._returnHighestLevel(stops)
                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)
                    if len(stops) > 1:
                        stops.remove(stopLevel)

                    if not stopLevel > entryPrice > profit:
                        profit = self.calculateProfit(entryPrice, highestStop, ratio)
                        stops.append(stopLevel)
                        stopLevel = highestStop
                        if not stopLevel > entryPrice > profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stopLevel, entryPrice))

            if mode == "moderat":
                if direction == "Buy":
                    stopLevel = 0
                    if len(stops) == 1:  # Only one TP level
                        stopLevel = stops[0]
                    elif len(stops) == 2:  # Two TP levels
                        stopLevel = stops[1]
                    else:  # Three or more TP levels
                        stopLevel = stops[3 * len(stops) // 4]  # Third quartile
                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)

                    if len(stops) > 1:
                        stops.remove(stopLevel)
                    if not stopLevel < entryPrice < profit:
                        profit = self.calculateProfit(entryPrice, lowestStop, ratio)
                        stops.append(stopLevel)
                        stopLevel = lowestStop
                        if not stopLevel < entryPrice > profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stopLevel, entryPrice))

                if direction == "Sell":
                    stopLevel = 0
                    # Handle midpoints
                    if len(stops) == 1:  # Only one TP level
                        stopLevel = stops[0]
                    elif len(stops) == 2:  # Two TP levels
                        stopLevel = stops[0]
                    else:  # Three or more TP levels
                        stopLevel = stops[len(stops) // 4]  # First quartile

                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)
                    if len(stops) > 1:
                        stops.remove(stopLevel)
                    if not stopLevel > entryPrice > profit:
                        profit = self.calculateProfit(entryPrice, highestStop, ratio)
                        stops.append(stopLevel)
                        stopLevel = highestStop
                        if not stopLevel > entryPrice > profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stopLevel, entryPrice))

            if mode == "safe":
                if direction == "Buy":
                    stopLevel = self._returnHighestLevel(stops)
                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)

                    if len(stops) > 1:
                        stops.remove(stopLevel)
                    if not stopLevel < entryPrice < profit:
                        profit = self.calculateProfit(entryPrice, lowestStop, ratio)
                        stops.append(stopLevel)
                        stopLevel = lowestStop
                        if not stopLevel < entryPrice < profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stopLevel, entryPrice))

                if direction == "Sell":
                    stopLevel = self._returnLowestLevel(stops)
                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)

                    if len(stops) > 1:
                        stops.remove(stopLevel)
                    if not stopLevel > entryPrice > profit:
                        profit = self.calculateProfit(entryPrice, highestStop, ratio)
                        stops.append(stopLevel)
                        stopLevel = highestStop
                        if not stopLevel > entryPrice > profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stopLevel, entryPrice))

        return profitStopEntryList
    
    def calculateEntriesByStopAndProfit(self, stop: list[float], profit: list[float], ratio: float, mode, direction)\
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

            if mode == "aggressive":
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

            if mode == "moderat":
                if direction == "Buy":
                    tpLevel = 0
                    if len(profit) == 1:  # Only one TP level
                        tpLevel = profit[0]
                    elif len(profit) == 2:  # Two TP levels
                        tpLevel = profit[1]
                    else:  # Three or more TP levels
                        tpLevel = profit[3 * len(profit) // 4]  # Third quartile
                    entry = self.calculateEntryPrice(stopPrice, tpLevel, ratio)

                    if len(profit) > 1:
                        profit.remove(tpLevel)
                    if not stopPrice < entry < tpLevel:
                        entry = self.calculateEntryPrice(stopPrice, highestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = highestTp
                        if not stopPrice < entry < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stopPrice, entry))

                if direction == "Sell":
                    tpLevel = 0
                    # Handle midpoints
                    if len(profit) == 1:  # Only one TP level
                        tpLevel = profit[0]
                    elif len(profit) == 2:  # Two TP levels
                        tpLevel = profit[0]
                    else:  # Three or more TP levels
                        tpLevel = profit[len(profit) // 4]  # First quartile

                    entry = self.calculateEntryPrice(stopPrice, tpLevel, ratio)

                    if len(profit) > 1:
                        profit.remove(tpLevel)
                    if not tpLevel < entry < stopPrice:
                        entry = self.calculateEntryPrice(stopPrice, lowestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = lowestTp
                        if not tpLevel < entry < stopPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stopPrice, entry))

            if mode == "safe":
                if direction == "Buy":
                    tpLevel = self._returnLowestLevel(profit)
                    entry = self.calculateEntryPrice(stopPrice, tpLevel, ratio)

                    if len(profit) > 1:
                        profit.remove(tpLevel)
                    if not stopPrice < entry < tpLevel:
                        entry = self.calculateEntryPrice(stopPrice, lowestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = lowestTp
                        if not stopPrice < entry < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stopPrice, entry))

                if direction == "Sell":
                    tpLevel = self._returnHighestLevel(profit)
                    entry = self.calculateEntryPrice(stopPrice, tpLevel, ratio)

                    if len(profit) > 1:
                        profit.remove(tpLevel)
                    if not tpLevel < entry < stopPrice:
                        entry = self.calculateEntryPrice(stopPrice, highestTp, ratio)
                        profit.append(tpLevel)
                        tpLevel = highestTp
                        if not tpLevel < entry < stopPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stopPrice, entry))

        return profitStopEntryList

    @staticmethod
    def _returnHighestLevel(referencePriceList:list[float]):
        index = 0
        tpLevel = 0
        for j in range(len(referencePriceList)):
            if referencePriceList[j] > tpLevel:
                tpLevel = referencePriceList[j]

        return tpLevel

    @staticmethod
    def _returnLowestLevel(referencePriceList:list[float]) -> float:
        index = 0
        tpLevel = 0
        for j in range(len(referencePriceList)):
            if j == 0:
                tpLevel = referencePriceList[j]
            if referencePriceList[j] < tpLevel:
                tpLevel = referencePriceList[j]

        return tpLevel
