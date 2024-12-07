from abc import abstractmethod, ABC

from Models.Pattern.Singleton.SingletonMeta import SingletonMeta


class Broker(ABC, metaclass=SingletonMeta):
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def sendRequest(self,endPoint,method,payload):
        pass
    @abstractmethod
    def genSignature(self,payload):
        pass
