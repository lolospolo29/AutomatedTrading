from abc import ABC

from files.models.trade.enums.Side import Side


class BaseRatio(ABC):
    """Basic Calculation of Profit/Stop/Entry"""
    # region Profit Stop Entry Calculation
    @staticmethod
    def calculate_profit(entry:float, stop: float, ratio: float) -> float:
            if stop < entry:
                profit =  (entry - stop) * ratio
                return profit + entry
            if stop > entry:
                profit =  (stop - entry) * ratio
                return entry - profit if entry - profit > 0 else entry
            if stop == entry:
                return entry

    @staticmethod
    def is_condition_full_filled(profit: float, stop: float, entry: float, side: str) -> bool:
            if side == Side.BUY:
                if stop < entry < profit:
                    return True
            if side == Side.SELL:
                if stop > entry > profit:
                    return True
            return False