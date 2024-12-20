from abc import ABC, abstractmethod

from Core.Main.Trade.OrderDirectionEnum import OrderDirection
from Core.Main.Trade.RiskFrameWorks.RiskModeEnum import RiskMode


class ModeRatioSort(ABC):
    @abstractmethod
    def sort(self,referenceList: list,mode: RiskMode,direction: OrderDirection):
        pass
