from abc import ABC, abstractmethod


class ITimeWindow(ABC):  # Entry / Exit Times
    @abstractmethod
    def IsInEntryWindow(self,time):
        pass

    @abstractmethod
    def IsInExitWindow(self,time):
        pass
