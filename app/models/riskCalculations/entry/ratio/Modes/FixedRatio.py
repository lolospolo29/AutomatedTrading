from typing import Tuple, Any

from app.models.riskCalculations.entry.ratio.Models.ProfitStopEntry import ProfitStopEntry
from app.models.riskCalculations.entry.ratio.Modes.BaseRatio import BaseRatio
from app.models.trade.OrderDirectionEnum import OrderDirection


class FixedRatio(BaseRatio):

    # region Single Fixed Ratio Input
    def calculateFixedRatioStop(self,entry: float,profit: float,ratio: float,direction: OrderDirection)-> Tuple[Any,bool]:
        stop = self.calculateStop(entry, profit, ratio)
        if  self.isConditionFullFilled(profit, stop, entry, direction):
            return ProfitStopEntry(profit, stop,entry),True
        else:
            return None,False

    def calculateFixedProfit(self, entry: float, stop: float, ratio: float, direction: OrderDirection)-> Tuple[Any,bool]:
        profit = self.calculateProfit(entry, stop, ratio)
        if self.isConditionFullFilled(profit,stop,entry, direction):
            return ProfitStopEntry(profit, stop,entry),True
        else:
            return None,False

    def calculateFixedEntry(self, stop: float, profit: float, ratio: float, direction: OrderDirection)-> Tuple[Any,bool]:
        entry = self.calculateEntry(stop, profit, ratio)
        if self.isConditionFullFilled(profit, stop, entry, direction):
            return ProfitStopEntry(profit, stop, entry),True
        else:
            return None,False
    # endregion

    # region List Fixed Ratio Input
    def calculateProfits(self, entries: list[float], stops: list[float], ratio: float,
                         direction: OrderDirection)-> list[ProfitStopEntry]:
        profitStopEntryList = []

        for i in range(len(entries)):
            for j in range(len(stops)):
                entry = entries[i]
                stop = stops[j]

                profit = self.calculateProfit(entry, stop, ratio)

                if not self.isConditionFullFilled(profit, stop, entry, direction):
                    continue

                profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

        return profitStopEntryList

    def calculateStops(self, entries: list[float], profits: list[float], ratio: float,
                       direction: OrderDirection)-> list[ProfitStopEntry]:

        profitStopEntryList = []

        for i in range(len(entries)):
            for j in range(len(profits)):
                entry = entries[i]
                profit = profits[j]

                stop = self.calculateStop(entry, profit, ratio)

                if not self.isConditionFullFilled(profit, stop, entry, direction):
                    continue

                profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

        return profitStopEntryList


    def calculateEntries(self, stops: list[float], profits: list[float], ratio: float,
                         direction: OrderDirection)-> list[ProfitStopEntry]:

        profitStopEntryList = []

        for i in range(len(stops)):
            for j in range(len(profits)):
                stop = stops[i]
                profit = profits[j]

                entry = self.calculateEntry(stop, profit, ratio)

                if not self.isConditionFullFilled(profit, stop, entry, direction):
                    continue

                profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

        return profitStopEntryList
    # endregion
