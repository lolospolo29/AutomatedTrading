from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.models.trade.Order import Order


class BrokerFacade:
    def __init__(self):
        self._bybit = BybitHandler()

    def sendSingleOrder(self,broker:str,order:Order):
        if broker == self._bybit.name:
            return self._bybit.placeOrder(order)
