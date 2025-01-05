from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.models.trade.Order import Order
from app.models.trade.RequestParameters import RequestParameters


class BrokerFacade:
    def __init__(self):
        self._bybitHandler = BybitHandler()

    def placeOrder(self, broker:str, order:Order):
        if broker == self._bybitHandler.name:
            return self._bybitHandler.placeOrder(order)

    def amendOrder(self,broker:str,order:Order):
        if broker == self._bybitHandler.name:
            return self._bybitHandler.amendOrder(order)

    def cancelOrder(self,broker:str,order:Order):
        if broker == self._bybitHandler.name:
            return self._bybitHandler.cancelOrder(order)

    def cancelAllOrders(self,broker:str,requestParameter:RequestParameters):
        if broker == self._bybitHandler.name:
            self._bybitHandler.cancelAllOrders(requestParameter.category, requestParameter.symbol,
                                               requestParameter.baseCoin, requestParameter.settleCoin,
                                               requestParameter.orderFilter, requestParameter.stopOrderType)

    def getOpenAndClosedOrders(self,broker:str,order:Order,requestParameter:RequestParameters):
        if broker == self._bybitHandler.name:
            self._bybitHandler.returnOpenAndClosedOrder(order, requestParameter.baseCoin, requestParameter.settleCoin,
                                                        requestParameter.openOnly, requestParameter.limit
                                                        , requestParameter.cursor)

    def getPositionInfo(self,broker:str,order: Order,requestParameter:RequestParameters):
        if broker == self._bybitHandler.name:
            self._bybitHandler.returnPositionInfo(order, requestParameter.baseCoin,
                                                  requestParameter.settleCoin, requestParameter.limit,
                                                  requestParameter.cursor)
