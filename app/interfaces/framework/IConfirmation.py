from abc import ABC, abstractmethod


class IConfirmation(ABC):
    @abstractmethod
    def return_confirmation(self, data_points):
        pass
