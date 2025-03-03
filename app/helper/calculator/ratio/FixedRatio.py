from typing import Tuple, Any

from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.helper.calculator.ratio.BaseRatio import BaseRatio
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class FixedRatio(BaseRatio):
    """Calculate Profit Stop Entry with a fixed ratio."""

    # region Single Fixed Ratio Input
    def calculate_fixed_ratio_stop(self, entry: float, profit: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        try:
            logger.debug("values :{},{},{}".format(entry, profit, ratio))
            stop = self.calculate_stop(entry, profit, ratio)
            if  self.is_condition_full_filled(profit, stop, entry, direction):
                return ProfitStopEntry(profit=profit, stop=stop, entry=entry),True
        except Exception as e:
            logger.error("Fixed Ratio Exception thrown,Error:{e}".format(e=e))

    def calculate_fixed_profit(self, entry: float, stop: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        try:
            logger.debug("values :{},{},{}".format(entry, stop, ratio))

            profit = self.calculate_profit(entry, stop, ratio)
            if self.is_condition_full_filled(profit, stop, entry, direction):
                return ProfitStopEntry(profit=profit,stop=stop,entry=entry),True
        except Exception as e:
            logger.error("Fixed Profit Exception thrown,Error:{e}".format(e=e))

    def calculate_fixed_entry(self, stop: float, profit: float, ratio: float, direction: OrderDirectionEnum)-> Tuple[Any,bool]:
        try:
            logger.debug("values :{},{},{}".format(profit, stop, ratio))

            entry = self.calculate_entry(stop, profit, ratio)
            if self.is_condition_full_filled(profit, stop, entry, direction):
                return ProfitStopEntry(profit=profit,stop=stop,entry=entry),True
        except Exception as e:
            logger.error("Fixed Entry Exception thrown,Error:{e}".format(e=e))
    # endregion

    # region List Fixed Ratio Input
    def calculate_profits(self, entries: list[float], stops: list[float], ratio: float,
                          direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        profitStopEntryList = []
        try:
            for i in range(len(entries)):
                try:
                    for j in range(len(stops)):
                        try:
                            entry = entries[i]
                            stop = stops[j]
                            logger.debug("values :{},{},{}".format(entry, stop, ratio))
                            profit = self.calculate_profit(entry, stop, ratio)

                            if not self.is_condition_full_filled(profit, stop, entry, direction):
                                continue

                            profitStopEntryList.append(ProfitStopEntry(profit=profit, stop=stop, entry=entry))
                        except Exception as e:
                            logger.warning("Profit Exception thrown,Error:{e}".format(e=e))
                        finally:
                            continue
                except Exception as e:
                    logger.warning("Profit Exception thrown,Error:{e}".format(e=e))
                finally:
                    continue

        except Exception as e:
            logger.exception("Profits Exception thrown,Error:{e}".format(e=e))
        finally:
            return profitStopEntryList

    def calculate_stops(self, entries: list[float], profits: list[float], ratio: float,
                        direction: OrderDirectionEnum)-> list[ProfitStopEntry]:

        profitStopEntryList = []
        try:
            for i in range(len(entries)):
                try:
                    for j in range(len(profits)):
                        try:
                            entry = entries[i]
                            profit = profits[j]
                            logger.debug("values :{},{},{}".format(entry, profit, ratio))

                            stop = self.calculate_stop(entry, profit, ratio)

                            if not self.is_condition_full_filled(profit, stop, entry, direction):
                                continue

                            profitStopEntryList.append(ProfitStopEntry(profit=profit, stop=stop, entry=entry))
                        except Exception as e:
                            logger.warning("Stops Exception thrown,Error:{e}".format(e=e))
                        finally:
                            continue
                except Exception as e:
                    logger.warning("Stops Exception thrown,Error:{e}".format(e=e))
                finally:
                    continue
            return profitStopEntryList
        except Exception as e:
            logger.exception("Stops Exception thrown,Error:{e}".format(e=e))
        finally:
            return profitStopEntryList


    def calculate_entries(self, stops: list[float], profits: list[float], ratio: float,
                          direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        profitStopEntryList = []
        try:
            for i in range(len(stops)):
                try:
                    for j in range(len(profits)):
                        try:
                            stop = stops[i]
                            profit = profits[j]
                            logger.debug("values :{},{},{}".format(stop, profit, ratio))
                            entry = self.calculate_entry(stop, profit, ratio)

                            if not self.is_condition_full_filled(profit, stop, entry, direction):
                                continue

                            profitStopEntryList.append(ProfitStopEntry(profit=profit, stop=stop, entry=entry))
                        except Exception as e:
                            logger.warning("Profit Exception thrown,Error:{e}".format(e=e))
                        finally:
                            continue
                except Exception as e:
                    logger.warning("Entries Exception throw,Error:{e}".format(e=e))
                finally:
                    continue
            return profitStopEntryList
        except Exception as e:
            logger.exception("Entries Exception thrown,Error:{e}".format(e=e))
        finally:
            return profitStopEntryList
    # endregion
