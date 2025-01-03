from abc import ABC, abstractmethod

from app.models.frameworks.PDArray import PDArray
from app.models.riskCalculations.RiskModeEnum import RiskMode
from app.models.trade.OrderDirectionEnum import OrderDirection


class IPDArray(ABC):  # Drill Fill CE
    @abstractmethod
    def returnCandleRange(self, data_points):
        pass

    @abstractmethod
    def returnArrayList(self, data_points):  # return list of possible entries
        pass

    @abstractmethod
    def returnStop(self,pdArray: PDArray,orderDirection: OrderDirection,riskMode: RiskMode):
        pass

    @abstractmethod
    def returnEntry(self,pdArray: PDArray,orderDirection: OrderDirection,riskMode: RiskMode):
        pass
