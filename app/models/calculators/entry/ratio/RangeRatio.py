from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.entry.ratio.BaseRatio import BaseRatio
from app.models.calculators.entry.ratio.FixedRatio import FixedRatio
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum

class RangeRatio(BaseRatio):

    def __init__(self):
        self.fixedRatio = FixedRatio()

    # region Single Range Ratio Input
    def calculate_range_profits(self, entry: float, stop: float, rangeRatio: list[float],
                                direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedProfits = []
        for ratio in rangeRatio:
            profit = self.calculate_profit(entry, stop, ratio)
            if self.is_condition_full_filled(profit, stop, entry, direction):
                estimatedProfits.append(ProfitStopEntry(profit,stop,entry))

        return estimatedProfits

    def calculate_range_stops(self, entry: float, profit: float, rangeRatio: list[float]
                              , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedStops = []
        for ratio in rangeRatio:
            stop = self.calculate_stop(entry, profit, ratio)
            if self.is_condition_full_filled(profit, stop, entry, direction):
                estimatedStops.append(ProfitStopEntry(profit,stop,entry))

        return estimatedStops

    def calculate_range_entries(self, stop: float, profit: float, rangeRatio: list[float]
                                , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedEntries = []
        for ratio in rangeRatio:
            entry = self.calculate_entry(stop, profit, ratio)
            if self.is_condition_full_filled(profit, stop, entry, direction):
                estimatedEntries.append(ProfitStopEntry(profit,stop,entry))

        return estimatedEntries
    # endregion

    # region List Range Ratio Input
    def calculate_profits(self, entries: list[float], stops: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for i  in range(len(entries)):
            entry = entries[i]
            for j in range(len(stops)):
                stop = stops[j]
                profitStopEntryList.extend(self.calculate_range_profits
                                           (entry, stop, rangeRatio, direction))

        return profitStopEntryList

    def calculate_stops(self, entries: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for i  in range(len(entries)):
            entry = entries[i]
            for j in range(len(profits)):
                profit = profits[j]
                profitStopEntryList.extend(self.calculate_range_stops
                                           (entry, profit, rangeRatio, direction))

        return profitStopEntryList

    def calculate_entries(self, stops: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        for i  in range(len(stops)):
            stop = stops[i]
            for j in range(len(profits)):
                profit = profits[j]
                profitStopEntryList.extend(self.calculate_range_entries
                                           (stop, profit, rangeRatio, direction))

        return profitStopEntryList
    # endregion
