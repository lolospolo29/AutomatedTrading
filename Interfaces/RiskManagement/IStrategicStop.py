from abc import ABC, abstractmethod


class IStrategicStop(ABC): # wo der Stop-Loss liegt (Swing,OB,End of Imbalance)
    @abstractmethod
    def getStrategyStop(self):
        pass
