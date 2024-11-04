from abc import ABC, abstractmethod


class IExitEntryStrategy(ABC):
    @abstractmethod
    def setPDArrays(self, PDArrays):
        pass

    @abstractmethod
    def setCallback(self, callback):
        pass

    @abstractmethod
    def applyRules(self):
        pass
