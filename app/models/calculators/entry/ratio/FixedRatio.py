from typing import Tuple, Any

from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.entry.ratio.BaseRatio import BaseRatio
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum


class FixedRatio(BaseRatio):

    # region Single Fixed Ratio Input
    def calculate_fixed_ratio_stop(self, entry: float, profit: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        stop = self.calculate_stop(entry, profit, ratio)
        if  self.is_condition_full_filled(profit, stop, entry, direction):
            return ProfitStopEntry(profit, stop,entry),True
        else:
            return None,False

    def calculate_fixed_profit(self, entry: float, stop: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        profit = self.calculate_profit(entry, stop, ratio)
        if self.is_condition_full_filled(profit, stop, entry, direction):
            return ProfitStopEntry(profit, stop,entry),True
        else:
            return None,False

    def calculate_fixed_entry(self, stop: float, profit: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        entry = self.calculate_entry(stop, profit, ratio)
        if self.is_condition_full_filled(profit, stop, entry, direction):
            return ProfitStopEntry(profit, stop, entry),True
        else:
            return None,False
    # endregion

    # region List Fixed Ratio Input
    def calculate_profits(self, entries: list[float], stops: list[float], ratio: float,
                          direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        profitStopEntryList = []

        for i in range(len(entries)):
            for j in range(len(stops)):
                entry = entries[i]
                stop = stops[j]

                profit = self.calculate_profit(entry, stop, ratio)

                if not self.is_condition_full_filled(profit, stop, entry, direction):
                    continue

                profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

        return profitStopEntryList

    def calculate_stops(self, entries: list[float], profits: list[float], ratio: float,
                        direction: OrderDirectionEnum)-> list[ProfitStopEntry]:

        profitStopEntryList = []

        for i in range(len(entries)):
            for j in range(len(profits)):
                entry = entries[i]
                profit = profits[j]

                stop = self.calculate_stop(entry, profit, ratio)

                if not self.is_condition_full_filled(profit, stop, entry, direction):
                    continue

                profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

        return profitStopEntryList


    def calculate_entries(self, stops: list[float], profits: list[float], ratio: float,
                          direction: OrderDirectionEnum)-> list[ProfitStopEntry]:

        profitStopEntryList = []

        for i in range(len(stops)):
            for j in range(len(profits)):
                stop = stops[i]
                profit = profits[j]

                entry = self.calculate_entry(stop, profit, ratio)

                if not self.is_condition_full_filled(profit, stop, entry, direction):
                    continue

                profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

        return profitStopEntryList
    # endregion
