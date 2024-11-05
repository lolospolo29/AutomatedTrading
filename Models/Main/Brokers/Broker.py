from abc import abstractmethod, ABC

from Models.Pattern.SingletonMeta import SingletonMeta


class Broker(ABC, metaclass=SingletonMeta):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def trailStop(self):
        pass
    @abstractmethod
    def cancelOrder(self):
        pass

    @abstractmethod
    def getOrderInformation(self):
        pass

    @abstractmethod
    def executeMarketOrder(self):
        pass

    @abstractmethod
    def setLimitOrder(self):
        pass

    @abstractmethod
    def getBalance(self):
        pass
