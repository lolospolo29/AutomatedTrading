from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.api.brokers.models.RequestParameters import RequestParameters
from app.interfaces.IBrokerHandler import IBrokerHandler


class BrokerFacade:
    def __init__(self):
        self.__registry:dict[str,IBrokerHandler]= {}
        __bh = BybitHandler()
        self.__register_handler(__bh.name, __bh)

    def __register_handler(self, broker:str, handler):
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
