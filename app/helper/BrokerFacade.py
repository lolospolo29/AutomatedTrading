from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.models.trade.Order import Order


class BrokerFacade:
    def __init__(self):
        self.__bybitHandler = BybitHandler()

    def sendSingleOrder(self,broker:str,order:Order):
        if broker == self.__bybitHandler.name:
            return self.__bybitHandler.placeOrder(order)
