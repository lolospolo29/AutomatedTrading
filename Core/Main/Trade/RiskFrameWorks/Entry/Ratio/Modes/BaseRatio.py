from abc import ABC

from Core.Main.Trade.OrderDirectionEnum import OrderDirection
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Models.ProfitStopEntry import ProfitStopEntry
from Core.Main.Trade.RiskFrameWorks.RiskModeEnum import RiskMode


class BaseRatio(ABC):
    # region Profit Stop Entry Calculation
    @staticmethod
    def calculateProfit(entry:float, stop: float, ratio: float) -> float:
        if stop < entry:
            profit =  (entry - stop) * ratio
            return profit + entry
        if stop > entry:
            profit =  (stop - entry) * ratio
            return entry - profit if entry - profit > 0 else entry
        if stop == entry:
            return entry

    @staticmethod
    def calculateStop(entry:float, profit: float, ratio: float):
        if profit > entry:
            stop = (profit - entry) / ratio
            return entry - stop if entry - stop > 0 else entry
        if profit < entry:
            stop = (entry - profit) / ratio
            return stop + entry
        if profit == entry:
            return entry

    @staticmethod
    def calculateEntry(stop:float, profit:float, ratio:float) -> float:
        if stop < profit:
            difference = profit - stop
            entry = difference / (ratio + 1)
            return entry + stop
        if stop > profit:
            difference = stop - profit
            entry = difference / (ratio + 1)
            return stop - entry if stop - entry > 0 else entry
        if stop == profit:
            return stop
    # endregion

    @staticmethod
    def isConditionFullFilled(profit: float, stop: float, entry: float,orderDirection: OrderDirection) -> bool:
        if orderDirection == OrderDirection.BUY:
            if stop < entry < profit:
                return True
        if orderDirection == OrderDirection.SELL:
            if stop > entry > profit:
                return True
        return False