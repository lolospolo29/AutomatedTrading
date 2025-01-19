from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.entry.ratio.BaseRatio import BaseRatio
from app.models.calculators.entry.ratio.FixedRatio import FixedRatio
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class RangeRatio(BaseRatio):
    """Calculate Profit Stop Entry for Range Ratio"""

    def __init__(self):
        self.fixedRatio = FixedRatio()

    # region Single Range Ratio Input
    def calculate_range_profits(self, entry: float, stop: float, rangeRatio: list[float],
                                direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedProfits = []
        try:
            for ratio in rangeRatio:
                profit = self.calculate_profit(entry, stop, ratio)
                if self.is_condition_full_filled(profit, stop, entry, direction):
                    estimatedProfits.append(ProfitStopEntry(profit,stop,entry))

        except Exception as e:
            logger.info("Profits Exception thrown")
        finally:
            return estimatedProfits

    def calculate_range_stops(self, entry: float, profit: float, rangeRatio: list[float]
                              , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedStops = []
        try:
            for ratio in rangeRatio:
                stop = self.calculate_stop(entry, profit, ratio)
                if self.is_condition_full_filled(profit, stop, entry, direction):
                    estimatedStops.append(ProfitStopEntry(profit,stop,entry))

        except Exception as e:
            logger.info("Stops Exception thrown")
        finally:
            return estimatedStops

    def calculate_range_entries(self, stop: float, profit: float, rangeRatio: list[float]
                                , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedEntries = []
        try:
            for ratio in rangeRatio:
                entry = self.calculate_entry(stop, profit, ratio)
                if self.is_condition_full_filled(profit, stop, entry, direction):
                    estimatedEntries.append(ProfitStopEntry(profit,stop,entry))
        except Exception as e:
            logger.info("Entries Exception thrown")

        return estimatedEntries
    # endregion

    # region List Range Ratio Input
    def calculate_profits(self, entries: list[float], stops: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        try:
            for i  in range(len(entries)):
                entry = entries[i]
                for j in range(len(stops)):
                    stop = stops[j]
                    profitStopEntryList.extend(self.calculate_range_profits
                                               (entry, stop, rangeRatio, direction))
        except Exception as e:
            logger.info("Profits Exception thrown")
        finally:
            return profitStopEntryList

    def calculate_stops(self, entries: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []
        try:
            for i  in range(len(entries)):
                entry = entries[i]
                for j in range(len(profits)):
                    profit = profits[j]
                    profitStopEntryList.extend(self.calculate_range_stops
                                               (entry, profit, rangeRatio, direction))
        except Exception as e:
            logger.info("Stops Exception thrown")
        finally:
            return profitStopEntryList

    def calculate_entries(self, stops: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []
        try:
            for i  in range(len(stops)):
                stop = stops[i]
                for j in range(len(profits)):
                    profit = profits[j]
                    profitStopEntryList.extend(self.calculate_range_entries
                                               (stop, profit, rangeRatio, direction))
        except Exception as e:
            logger.info("Entries Exception thrown")
        finally:
            return profitStopEntryList
    # endregion
