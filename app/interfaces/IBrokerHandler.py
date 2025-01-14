from abc import ABC, abstractmethod
from app.api.brokers.models.RequestParameters import RequestParameters
from app.api.brokers.models.BrokerOrder import BrokerOrder
from app.api.brokers.models.BrokerPosition import BrokerPosition


class IBrokerHandler(ABC):
    @abstractmethod
    def returnOpenAndClosedOrder(self, requestParams: RequestParameters) -> list[BrokerOrder]:
        """Retrieve open and closed orders."""
        pass

    @abstractmethod
    def returnPositionInfo(self, requestParams: RequestParameters) -> list[BrokerPosition]:
        """Retrieve position information."""
        pass

    @abstractmethod
    def returnOrderHistory(self, requestParams: RequestParameters) -> list[BrokerOrder]:
        """Retrieve order history."""
        pass

    @abstractmethod
    def amendOrder(self, requestParams: RequestParameters) -> BrokerOrder:
        """Amend an existing order."""
        pass

    @abstractmethod
    def cancelAllOrders(self, requestParams: RequestParameters) -> list[BrokerOrder]:
        """Cancel all orders."""
        pass

    @abstractmethod
    def cancelOrder(self, requestParams: RequestParameters) -> BrokerOrder:
        """Cancel a specific order."""
        pass

    @abstractmethod
    def placeOrder(self, requestParams: RequestParameters) -> BrokerOrder:
        """Place a new order."""
        pass

    @abstractmethod
    def setLeverage(self, requestParams: RequestParameters) -> bool:
        """Set leverage for a position."""
        pass
