from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.api.brokers.models.RequestParameters import RequestParameters
from app.interfaces.IBrokerHandler import IBrokerHandler


class BrokerFacade:
    def __init__(self):
        self._registry:dict[str,IBrokerHandler]= {}
        bh = BybitHandler()
        self.registerHandler(bh.name,bh)

    def registerHandler(self, broker:str,handler):
        self._registry[broker] = handler

    def placeOrder(self, requestParameter:RequestParameters):
        if requestParameter.broker.upper() in self._registry:
            return self._registry[requestParameter.broker].placeOrder(requestParameter)

    def amendOrder(self,requestParameter:RequestParameters):
        if requestParameter.broker.upper() in self._registry:
            return self._registry[requestParameter.broker].amendOrder(requestParameter)

    def cancelOrder(self,requestParameter:RequestParameters):
        if requestParameter.broker.upper() in self._registry:
            return self._registry[requestParameter.broker].cancelOrder(requestParameter)

    def cancelAllOrders(self,requestParameter:RequestParameters):
        if requestParameter.broker.upper() in self._registry:
            return self._registry[requestParameter.broker].cancelAllOrders(requestParameter)

    def returnOpenAndClosedOrders(self, requestParameter:RequestParameters):
        if requestParameter.broker.upper() in self._registry:
            return self._registry[requestParameter.broker].returnOpenAndClosedOrder(requestParameter)

    def returnPositionInfo(self, requestParameter:RequestParameters):
        if requestParameter.broker.upper() in self._registry:
            return self._registry[requestParameter.broker].returnPositionInfo(requestParameter)

    def returnOrderHistory(self, requestParameter:RequestParameters):
        if requestParameter.broker.upper() in self._registry:
            return self._registry[requestParameter.broker].returnOrderHistory(requestParameter)
