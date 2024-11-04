from abc import ABC, abstractmethod


class IRiskInvalidation(ABC):
    @abstractmethod
    def checkInvalidation(self):
        pass
