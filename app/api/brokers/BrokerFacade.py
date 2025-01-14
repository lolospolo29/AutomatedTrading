from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.api.brokers.models.RequestParameters import RequestParameters
from app.interfaces.IBrokerHandler import IBrokerHandler


class BrokerFacade:
    def __init__(self):
        self._registry:dict[str,IBrokerHandler]= {}
        self._bybitHandler = BybitHandler()

    def registerHandler(self, broker:str,handler):
        self._registry[broker] = handler

    def placeOrder(self, requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.placeOrder(requestParameter)

    def amendOrder(self,requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.amendOrder(requestParameter)

    def cancelOrder(self,requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.cancelOrder(requestParameter)

    def cancelAllOrders(self,requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.cancelAllOrders(requestParameter)

    def returnOpenAndClosedOrders(self, requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.returnOpenAndClosedOrder(requestParameter)

    def returnPositionInfo(self, requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.returnPositionInfo(requestParameter)

    def returnOrderHistory(self, requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.returnOrderHistory(requestParameter)
    # todo broker registry
    # environement test prod
    #