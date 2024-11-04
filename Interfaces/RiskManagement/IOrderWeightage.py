from abc import ABC, abstractmethod


class IOrderWeightage(ABC):
    @abstractmethod
    def getPercentagePerLevel(self):
        pass

    @abstractmethod
    def sortOrderToTPLevel(self):
        pass
