from abc import ABC, abstractmethod


class IConfirmation(ABC):
    @abstractmethod
    def getConfirmation(self, data_points):
        pass
