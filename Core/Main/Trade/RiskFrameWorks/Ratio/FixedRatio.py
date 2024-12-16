from Core.Main.Trade.RiskFrameWorks.Ratio.Models.ProfitStopEntry import ProfitStopEntry


class FixedRatio:

    @staticmethod
    def calculateProfit(entryPrice:float, stop: float, ratio: float) -> float:
        if stop < entryPrice:
            return (entryPrice - stop) * ratio
        if stop > entryPrice:
            return (stop - entryPrice) * ratio
        if stop == entryPrice:
            return 0

    @staticmethod
    def calculateStop(entryPrice:float, profitLevel: float, ratio: float):
        if profitLevel > entryPrice:
            return (profitLevel - entryPrice) / ratio
        if profitLevel < entryPrice:
            return (entryPrice - profitLevel) / ratio
        if profitLevel == entryPrice:
            return 0

    @staticmethod
    def calculateEntryPrice(stop:float, profitLevel:float, ratio:float) -> float:
        if stop < profitLevel:
            difference = profitLevel - stop
            return difference / (ratio + 1)
        if stop > profitLevel:
            difference = stop - profitLevel
            return difference / (ratio + 1)
        if stop == profitLevel:
            return 0

    def calculateStopsByProfitLevels(self,entryPrices: list[float], tpLevels: list[float], ratio: float,mode,direction)\
            -> list[ProfitStopEntry]:

        tpLevels.sort()
        highestTp = tpLevels[-1]  # Highest TP is the last in sorted order
        lowestTp = tpLevels[0]  # Lowest TP is the first in sorted order

        # Handle midpoints
        if len(tpLevels) == 1:  # Only one TP level
            midTpLowerHalf = tpLevels[0]
            midTpUpperHalf = tpLevels[0]
        elif len(tpLevels) == 2:  # Two TP levels
            midTpLowerHalf = tpLevels[0]
            midTpUpperHalf = tpLevels[1]
        else:  # Three or more TP levels
            midTpLowerHalf = tpLevels[len(tpLevels) // 4]  # First quartile
            midTpUpperHalf = tpLevels[3 * len(tpLevels) // 4]  # Third quartile

        if direction == "Buy":
            entryPrices.sort()
            tpLevels.sort()
        if direction == "Sell":
            entryPrices.sort(reverse=True)
            tpLevels.sort(reverse=True)

            # Initialize the results


        profitStopEntryList = []

        for i in range(len(entryPrices)):
            entryPrice = entryPrices[i]

            if mode == "aggressive":
                if direction == "Buy":
                    tpLevel = self.returnHighestLevel(tpLevels)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice - stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)

                    if not stop  < entryPrice < tpLevel:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        stop = entryPrice - stop
                        tpLevels.append(tpLevel)
                        tpLevel = highestTp
                        if not stop  < entryPrice < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = self.returnLowestLevel(tpLevels)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice + stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)

                    if not stop > entryPrice > tpLevel:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        stop = entryPrice + stop
                        tpLevels.append(tpLevel)
                        tpLevel = lowestTp
                        if not stop > entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

            if mode == "moderat":
                if direction == "Buy":
                    tpLevel = 0
                    if len(tpLevels) == 1:  # Only one TP level
                        tpLevel = tpLevels[0]
                    elif len(tpLevels) == 2:  # Two TP levels
                        tpLevel = tpLevels[1]
                    else:  # Three or more TP levels
                        tpLevel = tpLevels[3 * len(tpLevels) // 4]  # Third quartile
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice - stop

                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)
                    if not stop < entryPrice < tpLevel:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        stop = entryPrice - stop
                        tpLevels.append(tpLevel)
                        tpLevel = highestTp
                        if not stop < entryPrice < tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = 0
                    # Handle midpoints
                    if len(tpLevels) == 1:  # Only one TP level
                        tpLevel = tpLevels[0]
                    elif len(tpLevels) == 2:  # Two TP levels
                        tpLevel = tpLevels[0]
                    else:  # Three or more TP levels
                        tpLevel = tpLevels[len(tpLevels) // 4]  # First quartile

                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice + stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)
                    if not stop > entryPrice > tpLevel:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        stop = entryPrice + stop
                        tpLevels.append(tpLevel)
                        tpLevel = lowestTp
                        if not stop > entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

            if mode == "safe":
                if direction == "Buy":
                    tpLevel = self.returnLowestLevel(tpLevels)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice - stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)

                    if not stop < entryPrice < tpLevel:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        stop = entryPrice - stop
                        tpLevels.append(tpLevel)
                        tpLevel = highestTp
                        if not stop < entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = self.returnHighestLevel(tpLevels)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice + stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)

                    if not stop > entryPrice > tpLevel:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        stop = entryPrice + stop
                        tpLevels.append(tpLevel)
                        tpLevel = lowestTp
                        if not stop > entryPrice > tpLevel:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

        return profitStopEntryList

    def calculateProfitsByStopAndEntry(self, entryPrices: list[float], stops: list[float], ratio: float, mode, direction)\
            -> list[ProfitStopEntry]:

        stops.sort()
        highestStop = stops[-1]  # Highest Stop is the last in sorted order
        lowestStop = stops[0]  # Lowest Stop is the first in sorted order

        # Handle midpoints
        if len(stops) == 1:  # Only one TP level
            midStopLowerHalf = stops[0]
            midStopUpperHalf = stops[0]
        elif len(stops) == 2:  # Two TP levels
            midStopLowerHalf = stops[0]
            midStopUpperHalf = stops[1]
        else:  # Three or more TP levels
            midStopLowerHalf = stops[len(stops) // 4]  # First quartile
            midStopUpperHalf = stops[3 * len(stops) // 4]  # Third quartile

        if direction == "Buy":
            entryPrices.sort()
            stops.sort()
        if direction == "Sell":
            entryPrices.sort(reverse=True)
            stops.sort(reverse=True)

            # Initialize the results


        profitStopEntryList = []

        for i in range(len(entryPrices)):
            entryPrice = entryPrices[i]

            if mode == "aggressive":
                if direction == "Buy":
                    stopLevel = self.returnLowestLevel(stops)
                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)
                    profit = entryPrice + profit
                    if len(stops) > 1:
                        stops.remove(stopLevel)

                    if not stopLevel < entryPrice < profit :
                        profit = self.calculateProfit(entryPrice, lowestStop, ratio)
                        profit = entryPrice + profit
                        stops.append(stopLevel)
                        stopLevel = lowestStop
                        if not stopLevel < entryPrice < profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(stopLevel, profit, entryPrice))

                if direction == "Sell":
                    stopLevel = self.returnHighestLevel(stops)
                    profit = self.calculateProfit(entryPrice, stopLevel, ratio)
                    profit = entryPrice - profit
                    if len(stops) > 1:
                        stops.remove(stopLevel)

                    if not stopLevel > entryPrice > profit:
                        profit = self.calculateProfit(entryPrice, lowestStop, ratio)
                        profit = entryPrice - profit
                        stops.append(stopLevel)
                        stopLevel = lowestStop
                        if not stopLevel > entryPrice > profit:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(stopLevel, profit, entryPrice))

            if mode == "moderat":
                if direction == "Buy":
                    stopLevel = 0
                    if len(stops) == 1:  # Only one TP level
                        stopLevel = stops[0]
                    elif len(stops) == 2:  # Two TP levels
                        stopLevel = stops[1]
                    else:  # Three or more TP levels
                        stopLevel = stops[3 * len(stops) // 4]  # Third quartile
                    profit = self.calculateStop(entryPrice, stopLevel, ratio)
                    profit = entryPrice - profit

                    if len(stops) > 1:
                        stops.remove(stopLevel)
                    if profit > entryPrice or profit <= 0 or stopLevel < entryPrice or stopLevel == entryPrice:
                        profit = self.calculateStop(entryPrice, highestStop, ratio)
                        profit = entryPrice - profit
                        stops.append(stopLevel)
                        stopLevel = highestStop
                        if profit > entryPrice or profit <= 0 or stopLevel < entryPrice or stopLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(stopLevel, profit, entryPrice))

                if direction == "Sell":
                    stopLevel = 0
                    # Handle midpoints
                    if len(stops) == 1:  # Only one TP level
                        stopLevel = stops[0]
                    elif len(stops) == 2:  # Two TP levels
                        stopLevel = stops[0]
                    else:  # Three or more TP levels
                        stopLevel = stops[len(stops) // 4]  # First quartile

                    profit = self.calculateStop(entryPrice, stopLevel, ratio)
                    profit = entryPrice + profit
                    if len(stops) > 1:
                        stops.remove(stopLevel)
                    if profit < entryPrice or profit - entryPrice <= 0 or stopLevel > entryPrice or stopLevel == entryPrice:
                        profit = self.calculateStop(entryPrice, lowestStop, ratio)
                        profit = entryPrice + profit
                        stops.append(stopLevel)
                        stopLevel = lowestStop
                        if profit < entryPrice or profit - entryPrice <= 0 or stopLevel > entryPrice or stopLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(stopLevel, profit, entryPrice))

            if mode == "safe":
                if direction == "Buy":
                    stopLevel = self.returnLowestLevel(stops)
                    profit = self.calculateStop(entryPrice, stopLevel, ratio)
                    profit = entryPrice - profit
                    if len(stops) > 1:
                        stops.remove(stopLevel)

                    if profit > entryPrice or profit <= 0 or stopLevel < entryPrice or stopLevel == entryPrice:
                        profit = self.calculateStop(entryPrice, highestStop, ratio)
                        profit = entryPrice - profit
                        stops.append(stopLevel)
                        stopLevel = highestStop
                        if profit > entryPrice or profit <= 0 or stopLevel < entryPrice or stopLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(stopLevel, profit, entryPrice))

                if direction == "Sell":
                    stopLevel = self.returnHighestLevel(stops)
                    profit = self.calculateStop(entryPrice, stopLevel, ratio)
                    profit = entryPrice + profit
                    if len(stops) > 1:
                        stops.remove(stopLevel)

                    if profit < entryPrice or profit - entryPrice <= 0 or stopLevel > entryPrice or stopLevel == entryPrice:
                        profit = self.calculateStop(entryPrice, lowestStop, ratio)
                        profit = entryPrice + profit
                        stops.append(stopLevel)
                        stopLevel = lowestStop
                        if profit < entryPrice or profit - entryPrice <= 0 or stopLevel > entryPrice or stopLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(stopLevel, profit, entryPrice))

        return profitStopEntryList



    @staticmethod
    def returnHighestLevel(referencePriceList:list[float]):
        index = 0
        tpLevel = 0
        for j in range(len(referencePriceList)):
            if referencePriceList[j] > tpLevel:
                tpLevel = referencePriceList[j]

        return tpLevel

    @staticmethod
    def returnLowestLevel(referencePriceList:list[float]) -> float:
        index = 0
        tpLevel = 0
        for j in range(len(referencePriceList)):
            if j == 0:
                tpLevel = referencePriceList[j]
            if referencePriceList[j] < tpLevel:
                tpLevel = referencePriceList[j]

        return tpLevel

a = FixedRatio()
b = a.calculateProfit(200,100,4)
print(b)