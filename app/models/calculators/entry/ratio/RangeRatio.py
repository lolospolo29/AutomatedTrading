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
                try:
                    profit = self.calculate_profit(entry, stop, ratio)
                    logger.debug("values: {},{},{},{}".format(profit, stop,entry,ratio))
                    if self.is_condition_full_filled(profit, stop, entry, direction):
                        estimatedProfits.append(ProfitStopEntry(profit,stop,entry))
                except Exception as e:
                    logger.warning("Profit Range Exception thrown,error:{e}".format(e=e))
                finally:
                    continue

        except Exception as e:
            logger.exception("Profits Exception thrown")
        finally:
            return estimatedProfits

    def calculate_range_stops(self, entry: float, profit: float, rangeRatio: list[float]
                              , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedStops = []
        try:
            for ratio in rangeRatio:
                try:
                    stop = self.calculate_stop(entry, profit, ratio)
                    logger.debug("values: {},{},{},{}".format(profit, stop,entry,ratio))
                    if self.is_condition_full_filled(profit, stop, entry, direction):
                        estimatedStops.append(ProfitStopEntry(profit,stop,entry))
                except Exception as e:
                    logger.warning("Stop Range Exception thrown,error:{e}".format(e=e))

        except Exception as e:
            logger.exception("Stops Range Exception thrown,error:{e}".format(e=e))
        finally:
            return estimatedStops

    def calculate_range_entries(self, stop: float, profit: float, rangeRatio: list[float]
                                , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        estimatedEntries = []
        try:
            for ratio in rangeRatio:
                try:
                    entry = self.calculate_entry(stop, profit, ratio)
                    logger.debug("values: {},{},{},{}".format(profit, stop,entry,ratio))
                    if self.is_condition_full_filled(profit, stop, entry, direction):
                        estimatedEntries.append(ProfitStopEntry(profit,stop,entry))
                except Exception as e:
                    logger.warning("Entry Range Exception thrown,error:{e}".format(e=e))
        except Exception as e:
            logger.info("Entries Exception thrown,error:{e}".format(e=e))

        return estimatedEntries
    # endregion

    # region List Range Ratio Input
    def calculate_profits(self, entries: list[float], stops: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []

        try:
            for i  in range(len(entries)):
                try:
                    entry = entries[i]
                    for j in range(len(stops)):
                        try:
                            stop = stops[j]
                            logger.debug("values: {},{}".format(entry, stop))
                            profitStopEntryList.extend(self.calculate_range_profits
                                                       (entry, stop, rangeRatio, direction))
                        except Exception as e:
                            logger.warning("Entry Range Exception thrown,error:{e}".format(e=e))
                        finally:
                            continue
                except Exception as e:
                    logger.warning("Entry Range Exception thrown,error:{e}".format(e=e))
                finally:
                    continue
        except Exception as e:
            logger.exception("Profits Exception thrown,error:{e}".format(e=e))
        finally:
            return profitStopEntryList

    def calculate_stops(self, entries: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []
        try:
            for i  in range(len(entries)):
                try:
                    entry = entries[i]
                    for j in range(len(profits)):
                        try:
                            profit = profits[j]
                            logger.debug("values: {},{}".format(entry, profit))
                            profitStopEntryList.extend(self.calculate_range_stops
                                                       (entry, profit, rangeRatio, direction))
                        except Exception as e:
                            logger.warning("Stops Exception thrown,error:{e}".format(e=e))
                        finally:
                            continue
                except Exception as e:
                    logger.warning("Stops Exception thrown,error:{e}".format(e=e))
                finally:
                    continue
        except Exception as e:
            logger.exception("Stops Exception thrown,error:{e}".format(e=e))
        finally:
            return profitStopEntryList

    def calculate_entries(self, stops: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        profitStopEntryList:list[ProfitStopEntry] = []
        try:
            for i  in range(len(stops)):
                try:
                    stop = stops[i]
                    for j in range(len(profits)):
                        try:
                            profit = profits[j]
                            logger.debug("values: {},{}".format(stop, profit))
                            profitStopEntryList.extend(self.calculate_range_entries
                                                       (stop, profit, rangeRatio, direction))
                        except Exception as e:
                            logger.warning("Entries Range Exception thrown,error:{e}".format(e=e))
                except Exception as e:
                    logger.warning("Entries Range Exception thrown,error:{e}".format(e=e))
        except Exception as e:
            logger.exception("Entries Exception thrown,error:{e}".format(e=e))
        finally:
            return profitStopEntryList
    # endregion
