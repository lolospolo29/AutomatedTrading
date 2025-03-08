from files.api.brokers.models.RequestParameters import RequestParameters
from files.interfaces.IBrokerHandler import IBrokerHandler


class BrokerRegistry:
    """
    Acts as a centralized facade for managing and delegating broker-related operations across supported brokers.

    The BrokerFacade class simplifies interactions with multiple brokers by maintaining a registry
    of broker handlers and delegating various operations such as placing orders, amending orders,
    canceling orders, and retrieving order or position information to the corresponding broker
    handlers. The class provides a unified API to execute these operations, reducing the complexity
    of handling broker-specific logic across multiple systems.

    :ivar __registry: A private dictionary that maps broker names to their corresponding broker
        handler instances.
    :type __registry: dict[str, IBrokerHandler]
    """
    def __init__(self):
        self.__registry:dict[str,IBrokerHandler]= {}

    def register_handler(self, broker:str, handler:IBrokerHandler):
        self.__registry[broker] = handler

    def place_order(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].place_order(request_params)

    def amend_order(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].amend_order(request_params)

    def cancel_order(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].cancel_order(request_params)

    def cancel_all_orders(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].cancel_all_orders(request_params)

    def return_open_and_closed_orders(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].return_open_and_closed_order(request_params)

    def return_position_info(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].return_position_info(request_params)

    def return_order_history(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].return_order_history(request_params)

    def set_leverage(self, request_params:RequestParameters):
        if request_params.broker.upper() in self.__registry:
            return self.__registry[request_params.broker].set_leverage(request_params)
