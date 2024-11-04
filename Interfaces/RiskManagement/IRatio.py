from abc import ABC, abstractmethod


class IRatio(ABC): # Fixed or Variable
    @abstractmethod
    def isRatioValid(self):
        pass
    @abstractmethod
    def getRatio(self):
        pass
