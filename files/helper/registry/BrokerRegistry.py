from files.models.broker.RequestParameters import RequestParameters
from files.interfaces.IBrokerHandler import IBrokerHandler


class BrokerRegistry:
    def __init__(self):
        self._registry:dict[str,IBrokerHandler]= {}

    def register_handler(self,handler:IBrokerHandler):
        self._registry[handler.name.upper()] = handler

    def place_order(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].place_order(request_params)

    def amend_order(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].amend_order(request_params)

    def cancel_order(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].cancel_order(request_params)

    def cancel_all_orders(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].cancel_all_orders(request_params)

    def return_open_and_closed_orders(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].return_open_and_closed_order(request_params)

    def return_position_info(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].return_position_info(request_params)

    def return_order_history(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].return_order_history(request_params)

    def set_leverage(self, request_params:RequestParameters):
        if request_params.broker.upper() in self._registry:
            return self._registry[request_params.broker].set_leverage(request_params)
