from abc import ABC, abstractmethod


class IBroker(ABC):
    @abstractmethod
    def getBalance(self):
        pass

    @abstractmethod
    def setLimitOrder(self):
        pass

    @abstractmethod
    def executeMarketOrder(self):
        pass

    @abstractmethod
    def getOrdeInformation(self):
        pass

    @abstractmethod
    def cancelOrder(self):
        pass

    @abstractmethod
    def trailStop(self):
        pass



