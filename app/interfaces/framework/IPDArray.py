from abc import ABC, abstractmethod

from app.models.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum


class IPDArray(ABC):  # Drill Fill CE
    @abstractmethod
    def return_candle_range(self, data_points):
        pass

    @abstractmethod
    def return_pd_arrays(self, data_points):  # return list of possible entries
        pass

    @abstractmethod
    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode):
        pass

    @abstractmethod
    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode):
        pass
