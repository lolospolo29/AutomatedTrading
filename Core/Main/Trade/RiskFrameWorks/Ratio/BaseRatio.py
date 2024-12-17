from abc import ABC


class BaseRatio(ABC):
    @staticmethod
    def calculateProfit(entry:float, stop: float, ratio: float) -> float:
        if stop < entry:
            return (entry - stop) * ratio
        if stop > entry:
            return (stop - entry) * ratio
        if stop == entry:
            return 0

    @staticmethod
    def calculateStop(entry:float, profit: float, ratio: float):
        if profit > entry:
            return (profit - entry) / ratio
        if profit < entry:
            return (entry - profit) / ratio
        if profit == entry:
            return 0

    @staticmethod
    def calculateEntryPrice(stop:float, profit:float, ratio:float) -> float:
        if stop < profit:
            difference = profit - stop
            return difference / (ratio + 1)
        if stop > profit:
            difference = stop - profit
            return difference / (ratio + 1)
        if stop == profit:
            return 0