from abc import ABC, abstractmethod


class IPDArray(ABC):  # Drill Fill CE
    @abstractmethod
    def returnCandleRange(self, data_points):
        pass

    @abstractmethod
    def returnArrayList(self, data_points):  # return list of possible entrys
        pass
