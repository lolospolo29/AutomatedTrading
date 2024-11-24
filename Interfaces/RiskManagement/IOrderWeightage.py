from abc import ABC, abstractmethod


class IOrderWeightage(ABC):
    @abstractmethod
    def getPercentagePerLevel(self, percentage: float, order_tp_assignments: list[tuple[int, float]], mode: int):
        pass

    @abstractmethod
    def sortOrderToTPLevel(self, orderAmount: int, tpLevel: list[float], direction: str,mode: int):
        pass
