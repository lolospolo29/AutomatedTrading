from app.api.brokers.bybit.BybitHandler import BybitHandler
from app.api.brokers.bybit.enums.OpenOnlyEnum import OpenOnlyEnum
from app.api.brokers.bybit.enums.OrderFilterEnum import OrderFilterEnum
from app.models.trade.CategoryEnum import CategoryEnum
from app.models.trade.Order import Order


class BrokerFacade:
    def __init__(self):
        self.__bybitHandler = BybitHandler()

    def placeOrder(self, broker:str, order:Order):
        if broker == self.__bybitHandler.name:
            return self.__bybitHandler.placeOrder(order)

    def amendOrder(self,broker:str,order:Order):
        if broker == self.__bybitHandler.name:
            return self.__bybitHandler.amendOrder(order)

    def cancelOrder(self,broker:str,order:Order):
        if broker == self.__bybitHandler.name:
            return self.__bybitHandler.cancelOrder(order)

    def cancelAllOrders(self,broker:str,category:CategoryEnum=None,symbol:str=None,baseCoin:str=None,settleCoin:str=None,
                        orderFilter:OrderFilterEnum=None,stopOrderType:bool=False):
        if broker == self.__bybitHandler.name:
            self.__bybitHandler.cancelAllOrders(category,symbol,baseCoin,settleCoin,orderFilter,stopOrderType)

    def getOpenAndClosedOrders(self,broker:str,order:Order,baseCoin:str=None,settleCoin:str=None,
                               openOnly:OpenOnlyEnum=None
                                 ,limit:int=20,cursor:str=None):
        if broker == self.__bybitHandler.name:
            self.__bybitHandler.returnOpenAndClosedOrder(order,baseCoin,settleCoin,openOnly,limit,cursor)

    def getPositionInfo(self,broker:str,order: Order,baseCoin:str=None,settleCoin:str=None
                                 ,limit:int=20,cursor:str=None):
        if broker == self.__bybitHandler.name:
            self.__bybitHandler.returnPositionInfo(order,baseCoin,settleCoin,limit,cursor)
