from abc import ABC, abstractmethod


class IFactory(ABC):
    @abstractmethod
    def returnClass(self,typ):
        pass