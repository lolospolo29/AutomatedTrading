from abc import ABC, abstractmethod


class ITimeWindow(ABC):  # Entry / Exit Times
    @abstractmethod
    def IsInEntryWindow(self):
        pass

    @abstractmethod
    def IsInExitWindow(self):
        pass
