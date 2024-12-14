from abc import ABC, abstractmethod

from Core.Main.Asset.SubModels.Candle import Candle


class IStrategicStop(ABC): # wo der Stop-Loss liegt (Swing,OB,End of Imbalance)
    @abstractmethod
    def getStrategyStop(self, candle: Candle):
        pass
