from abc import ABC, abstractmethod


class IPDArray(ABC):  # Drill Fill CE
    @abstractmethod
    def getCandleRange(self, data_points):
        pass

    @abstractmethod
    def getArrayList(self, data_points):  # return list of possible entrys
        pass
