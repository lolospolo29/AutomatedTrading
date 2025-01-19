from typing import Tuple, Any

from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.entry.ratio.BaseRatio import BaseRatio
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class FixedRatio(BaseRatio):
    """Calculate Profit Stop Entry with a fixed ratio."""

    # region Single Fixed Ratio Input
    def calculate_fixed_ratio_stop(self, entry: float, profit: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        try:
            stop = self.calculate_stop(entry, profit, ratio)
            if  self.is_condition_full_filled(profit, stop, entry, direction):
                return ProfitStopEntry(profit, stop,entry),True
        except Exception as e:
            logger.info("Fixed Ratio Exception thrown")
        finally:
            return None,False

    def calculate_fixed_profit(self, entry: float, stop: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        try:
            profit = self.calculate_profit(entry, stop, ratio)
            if self.is_condition_full_filled(profit, stop, entry, direction):
                return ProfitStopEntry(profit, stop,entry),True
        except Exception as e:
            logger.info("Fixed Profit Exception thrown")
        finally:
            return None,False

    def calculate_fixed_entry(self, stop: float, profit: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        try:
            entry = self.calculate_entry(stop, profit, ratio)
            if self.is_condition_full_filled(profit, stop, entry, direction):
                return ProfitStopEntry(profit, stop, entry),True
        except Exception as e:
            logger.info("Fixed Entry Exception thrown")
        finally:
            return None,False
    # endregion

    # region List Fixed Ratio Input
    def calculate_profits(self, entries: list[float], stops: list[float], ratio: float,
                          direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        profitStopEntryList = []
        try:
            for i in range(len(entries)):
                for j in range(len(stops)):
                    entry = entries[i]
                    stop = stops[j]

                    profit = self.calculate_profit(entry, stop, ratio)

                    if not self.is_condition_full_filled(profit, stop, entry, direction):
                        continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

        except Exception as e:
            logger.info("Profits Exception thrown")
        finally:
            return profitStopEntryList

    def calculate_stops(self, entries: list[float], profits: list[float], ratio: float,
                        direction: OrderDirectionEnum)-> list[ProfitStopEntry]:

        profitStopEntryList = []
        try:
            for i in range(len(entries)):
                for j in range(len(profits)):
                    entry = entries[i]
                    profit = profits[j]

                    stop = self.calculate_stop(entry, profit, ratio)

                    if not self.is_condition_full_filled(profit, stop, entry, direction):
                        continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

            return profitStopEntryList
        except Exception as e:
            logger.info("Stops Exception thrown")
        finally:
            return profitStopEntryList


    def calculate_entries(self, stops: list[float], profits: list[float], ratio: float,
                          direction: OrderDirectionEnum)-> list[ProfitStopEntry]:

        profitStopEntryList = []

        try:
            for i in range(len(stops)):
                for j in range(len(profits)):
                    stop = stops[i]
                    profit = profits[j]

                    entry = self.calculate_entry(stop, profit, ratio)

                    if not self.is_condition_full_filled(profit, stop, entry, direction):
                        continue

                    profitStopEntryList.append(ProfitStopEntry(profit, stop, entry))

            return profitStopEntryList
        except Exception as e:
            logger.info("Entries Exception thrown")
        finally:
            return profitStopEntryList
    # endregion
