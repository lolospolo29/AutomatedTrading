from abc import ABC


class BaseRatio(ABC):
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
    def calculateEntryPrice(stop:float, profit:float, ratio:float) -> float:
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

