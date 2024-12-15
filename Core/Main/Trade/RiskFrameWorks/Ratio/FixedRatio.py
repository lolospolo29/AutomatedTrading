from Core.Main.Trade.RiskFrameWorks.Ratio.ProfitStopEntry import ProfitStopEntry


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
            return difference * (ratio / 100)
        if stop > profitLevel:
            difference = stop - profitLevel
            return difference * (ratio / 100)
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

                    if stop > entryPrice or stop <= 0 or tpLevel < entryPrice or tpLevel == entryPrice:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        stop = entryPrice - stop
                        tpLevels.append(tpLevel)
                        tpLevel = highestTp
                        if stop > entryPrice or stop <= 0 or tpLevel < entryPrice or tpLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = self.returnLowestLevel(tpLevels)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice + stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)

                    if stop < entryPrice or stop - entryPrice <= 0 or tpLevel > entryPrice or tpLevel == entryPrice:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        stop = entryPrice + stop
                        tpLevels.append(tpLevel)
                        tpLevel = lowestTp
                        if stop < entryPrice or stop - entryPrice <= 0 or tpLevel > entryPrice or tpLevel == entryPrice:
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
                    if stop > entryPrice or stop <= 0 or tpLevel < entryPrice or tpLevel == entryPrice:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        stop = entryPrice - stop
                        tpLevels.append(tpLevel)
                        tpLevel = highestTp
                        if stop > entryPrice or stop <= 0 or tpLevel < entryPrice or tpLevel == entryPrice:
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
                    if stop < entryPrice or stop - entryPrice <= 0 or tpLevel > entryPrice or tpLevel == entryPrice:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        stop = entryPrice + stop
                        tpLevels.append(tpLevel)
                        tpLevel = lowestTp
                        if stop < entryPrice or stop - entryPrice <= 0 or tpLevel > entryPrice or tpLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

            if mode == "safe":
                if direction == "Buy":
                    tpLevel = self.returnLowestLevel(tpLevels)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice - stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)

                    if stop > entryPrice or stop <= 0 or tpLevel < entryPrice or tpLevel == entryPrice:
                        stop = self.calculateStop(entryPrice, highestTp, ratio)
                        stop = entryPrice - stop
                        tpLevels.append(tpLevel)
                        tpLevel = highestTp
                        if stop > entryPrice or stop <= 0 or tpLevel < entryPrice or tpLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

                if direction == "Sell":
                    tpLevel = self.returnHighestLevel(tpLevels)
                    stop = self.calculateStop(entryPrice, tpLevel, ratio)
                    stop = entryPrice + stop
                    if len(tpLevels) > 1:
                        tpLevels.remove(tpLevel)

                    if stop < entryPrice or stop - entryPrice <= 0 or tpLevel > entryPrice or tpLevel == entryPrice:
                        stop = self.calculateStop(entryPrice, lowestTp, ratio)
                        stop = entryPrice + stop
                        tpLevels.append(tpLevel)
                        tpLevel = lowestTp
                        if stop < entryPrice or stop - entryPrice <= 0 or tpLevel > entryPrice or tpLevel == entryPrice:
                            continue

                    profitStopEntryList.append(ProfitStopEntry(tpLevel, stop, entryPrice))

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
