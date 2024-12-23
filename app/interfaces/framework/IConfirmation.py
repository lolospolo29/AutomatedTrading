from abc import ABC, abstractmethod


class IConfirmation(ABC):
    @abstractmethod
    def returnConfirmation(self, data_points):
        pass
