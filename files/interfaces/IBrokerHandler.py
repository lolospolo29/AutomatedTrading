from abc import ABC, abstractmethod
from files.api.brokers.models.RequestParameters import RequestParameters
from files.api.brokers.models.BrokerOrder import BrokerOrder
from files.api.brokers.models.BrokerPosition import BrokerPosition


class IBrokerHandler(ABC):

    @abstractmethod
    def return_name(self)->str:
        pass

    @abstractmethod
    def return_open_and_closed_order(self, request_params: RequestParameters) -> list[BrokerOrder]:
        """Retrieve open and closed orders."""
        pass

    @abstractmethod
    def return_position_info(self, request_params: RequestParameters) -> list[BrokerPosition]:
        """Retrieve position information."""
        pass

    @abstractmethod
    def return_order_history(self, request_params: RequestParameters) -> list[BrokerOrder]:
        """Retrieve order history."""
        pass

    @abstractmethod
    def amend_order(self, request_params: RequestParameters) -> BrokerOrder:
        """Amend an existing order."""
        pass

    @abstractmethod
    def cancel_all_orders(self, request_params: RequestParameters) -> list[BrokerOrder]:
        """Cancel all orders."""
        pass

    @abstractmethod
    def cancel_order(self, request_params: RequestParameters) -> BrokerOrder:
        """Cancel a specific order."""
        pass

    @abstractmethod
    def place_order(self, request_params: RequestParameters) -> BrokerOrder:
        """Place a new order."""
        pass

    @abstractmethod
    def set_leverage(self, requestParams: RequestParameters) -> bool:
        """Set leverage for a position."""
        pass
