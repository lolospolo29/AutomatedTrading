from abc import ABC, abstractmethod


class ITakeProfitStrategy(ABC): # wo der Stop-Loss liegt
    @abstractmethod
    def returnExitList(self): # pass what to search for FVG,OB,Swing
        pass
    @abstractmethod
    def returnLastExit(self): # return Last Exit
        pass
