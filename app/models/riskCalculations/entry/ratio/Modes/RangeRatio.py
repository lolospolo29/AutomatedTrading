from app.models.riskCalculations.entry.ratio.Models.ProfitStopEntry import ProfitStopEntry
from app.models.riskCalculations.entry.ratio.Modes.BaseRatio import BaseRatio
from app.models.riskCalculations.entry.ratio.Modes.FixedRatio import FixedRatio
from app.models.trade.OrderDirectionEnum import OrderDirection

class RangeRatio(BaseRatio):

    def __init__(self):
        self.fixedRatio = FixedRatio()

    # region Single Range Ratio Input
    def calculateRangeProfits(self, entry: float, stop: float, rangeRatio: list[float],
                              direction: OrderDirection) -> list[ProfitStopEntry]:
        estimatedProfits = []
        for ratio in rangeRatio:
            profit = self.calculateProfit(entry, stop, ratio)
            if self.isConditionFullFilled(profit, stop, entry, direction):
                estimatedProfits.append(ProfitStopEntry(profit,stop,entry))

        return estimatedProfits

    def calculateRangeStops(self, entry: float, profit: float, rangeRatio: list[float]
                            , direction: OrderDirection) -> list[ProfitStopEntry]:
        estimatedStops = []
        for ratio in rangeRatio:
            stop = self.calculateStop(entry, profit, ratio)
            if self.isConditionFullFilled(profit,stop,entry, direction):
                estimatedStops.append(ProfitStopEntry(profit,stop,entry))

        return estimatedStops

    def calculateRangeEntries(self, stop: float, profit: float, rangeRatio: list[float]
                              , direction: OrderDirection) -> list[ProfitStopEntry]:
        estimatedEntries = []
        for ratio in rangeRatio:
            entry = self.calculateEntry(stop, profit, ratio)
            if self.isConditionFullFilled(profit,stop,entry, direction):
                estimatedEntries.append(ProfitStopEntry(profit,stop,entry))

        return estimatedEntries
    # endregion

    # region List Range Ratio Input
    def calculateProfits(self, entries: list[float], stops: list[float], rangeRatio:
    list[int], direction: OrderDirection) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for i  in range(len(entries)):
            entry = entries[i]
            for j in range(len(stops)):
                stop = stops[j]
                profitStopEntryList.extend(self.calculateRangeProfits
                                           (entry, stop, rangeRatio, direction))

        return profitStopEntryList

    def calculateStops(self, entries: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirection) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for i  in range(len(entries)):
            entry = entries[i]
            for j in range(len(profits)):
                profit = profits[j]
                profitStopEntryList.extend(self.calculateRangeStops
                                           (entry, profit, rangeRatio, direction))

        return profitStopEntryList

    def calculateEntries(self, stops: list[float], profits: list[float], rangeRatio:
    list[int],direction: OrderDirection) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for i  in range(len(stops)):
            stop = stops[i]
            for j in range(len(profits)):
                profit = profits[j]
                profitStopEntryList.extend(self.calculateRangeEntries
                                           (stop, profit, rangeRatio, direction))

        return profitStopEntryList
    # endregion
