from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.api.brokers.RequestParameters import RequestParameters


class BrokerFacade:
    def __init__(self):
        self._bybitHandler = BybitHandler()

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

    def getOpenAndClosedOrders(self,requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.returnOpenAndClosedOrder(requestParameter)

    def getPositionInfo(self,requestParameter:RequestParameters):
        if requestParameter.broker == self._bybitHandler.name:
            return self._bybitHandler.returnPositionInfo(requestParameter)
    # todo broker registry
    # environement test prod
    #