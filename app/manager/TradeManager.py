import threading
import uuid
from threading import Thread

from app.api.brokers.bybit.reponse.get.OpenAndClosedOrdersAll import OpenAndClosedOrdersAll
from app.api.brokers.bybit.reponse.get.PositionInfoAll import PositionInfoAll
from app.api.brokers.bybit.reponse.post.PlaceOrderAll import PlaceOrderAll
from app.db.modules.mongoDBTrades import mongoDBTrades
from app.helper.BrokerFacade import BrokerFacade
from app.helper.registry.LockRegistry import LockRegistry
from app.helper.registry.TradeSemaphoreRegistry import TradeSemaphoreRegistry
from app.manager.RiskManager import RiskManager
from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.AssetClassEnum import AssetClassEnum
from app.models.trade.Order import Order
from app.models.trade.OrderDirectionEnum import OrderDirection
from app.models.trade.OrderStatusEnum import OrderStatusEnum
from app.models.trade.OrderTypeEnum import OrderTypeEnum
from app.models.trade.RequestParameters import RequestParameters
from app.models.trade.Trade import Trade


class TradeManager:

    # region Initializing
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradeManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._TradeRegistry = TradeSemaphoreRegistry()
            self._LockRegistry = LockRegistry()
            self.openTrades:dict[str,Trade] = {}
            self._mongoDBTrades: mongoDBTrades = mongoDBTrades()
            self._BrokerFacade = BrokerFacade()
            self._RiskManager: RiskManager = RiskManager()
            self._initialized = True  # Markiere als initialisiert
    # endregion

    # region Register Remove Dict
    def registerTrade(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                self._TradeRegistry.register_relation(trade.relation)
                self._TradeRegistry.acquire_trade(trade.relation)
                if trade.id not in self.openTrades:
                    self.openTrades[trade.id] = trade
                    print(f"Trade for '{trade.relation.broker}' "
                          f"with ID: {trade.id} created and added to the Trade Manager.")

    def removeTrade(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self.openTrades.pop(trade.id)
    # endregion

    # region CRUD DB
    def findTradeOrTradesInDB(self,trade:Trade=None) -> list[Trade]:
        with self._lock:
            if trade is None:
                return self._mongoDBTrades.findTradeOrTradesById()
            else:
                return self._mongoDBTrades.findTradeOrTradesById(trade.id)

    def findOrderOrOrdersInDB(self,order:Order=None) -> list[Order]:
        if order is None:
            return self._mongoDBTrades.findOrderOrOrdersById()
        else:
            return self._mongoDBTrades.findOrderOrOrdersById(order.orderLinkId)

    def writeTradeToDB(self, trade: Trade):
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self._mongoDBTrades.addTradeToDB(trade)

    def updateTradInDB(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self._mongoDBTrades.updateTrade(trade)

    def archiveTradeInDB(self, trade: Trade) -> None:
        with self._lock:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    self._mongoDBTrades.archiveTrade(trade)

    def writeOrderToDB(self, order: Order) -> None:
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
                self._mongoDBTrades.addOrderToDB(order)

    def updateOrderInDB(self, order: Order) -> None:
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            self._mongoDBTrades.updateOrder(order)

    def archiveOrderInDB(self, order: Order) -> None:
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            self._mongoDBTrades.archiveOrder(order)
    # endregion

    # region API Requests
    def placeTrade(self, trade: Trade,assetClass:str) -> None:
            tradeLock = self._LockRegistry.get_lock(trade.id)
            with tradeLock:
                if trade.id in self.openTrades:
                    trade = self.openTrades[trade.id]
                    from multiprocessing.pool import ThreadPool
                    pool = ThreadPool(processes=len(trade.orders))
                    asyncPlaceOrderResults = []
                    for order in trade.orders:
                        placeOrderAsync = pool.apply_async(self.placeOrder, (trade.relation.broker,assetClass,order))
                        asyncPlaceOrderResults.append(placeOrderAsync)
                        # do some other stuff in the main process

                    for placeOrderAsync in asyncPlaceOrderResults:
                        orderResult = placeOrderAsync.get()# get the return value from your function.
                        if isinstance(orderResult, Exception):
                            print("Order Failed with Trade-ID"+trade.id)

                    asyncOpenAndClosedResults = []

                    for order in trade.orders:

                        openAndClosedAsync = pool.apply_async(self.getOpenAndClosedOrders,
                                                        (trade.relation.broker,order,RequestParameters()))
                        asyncOpenAndClosedResults.append(openAndClosedAsync)
                        # todo map res to order

                    for openAndClosedAsync in asyncOpenAndClosedResults:
                        ocResult:OpenAndClosedOrdersAll = openAndClosedAsync.get()  # get the return value from your function.
                        if isinstance(ocResult, Exception):
                            print("Order Failed with Trade-ID" + trade.id)


                    asyncPositionInfoResults = []

                    for order in trade.orders:

                        positionInfoAsync = pool.apply_async(self.getPositionInfo,
                                                        (trade.relation.broker,order,RequestParameters()))
                        asyncPositionInfoResults.append(positionInfoAsync)
                        # todo map res to order

                    for positionInfosAsync in asyncPositionInfoResults:
                        pIResult:PositionInfoAll = positionInfosAsync.get()
                        if isinstance(pIResult, Exception):
                            print("Order Failed with Trade-ID" + trade.id)



    def placeOrder(self,broker:str,assetClass:str,order: Order):
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            if order.orderType == OrderTypeEnum.MARKET.value:
                order.qty = str(self._calculateQtyMarket(assetClass, order))
            if order.orderType == OrderTypeEnum.LIMIT.value:
                order.qty = str(self._calculateQtyLimit(assetClass, order))
            res:PlaceOrderAll = self._BrokerFacade.placeOrder(broker, order)
            order.orderId = res.orderId
        return order

    def amendOrder(self,broker:str,order:Order):
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            order = self._BrokerFacade.amendOrder(broker, order)

    def cancelOrder(self,broker:str,order:Order):
        orderLock = self._LockRegistry.get_lock(order.orderLinkId)
        with orderLock:
            order = self._BrokerFacade.amendOrder(broker, order)


    def getOpenAndClosedOrders(self,broker:str,order:Order,requestParameter:RequestParameters):
        return self._BrokerFacade.getOpenAndClosedOrders(broker,order,requestParameter)

    def getPositionInfo(self,broker:str, order:Order,requestParameters:RequestParameters):
        return self._BrokerFacade.getPositionInfo(broker, order,requestParameters)

    # endregion

    # region Risk Management

    def _calculateQtyMarket(self, assetClass:str, order:Order)->float:
        moneyatrisk = self._RiskManager.calculate_money_at_risk()
        order.moneyAtRisk = moneyatrisk
        qty = 0.00
        if order.orderType == OrderTypeEnum.MARKET.value:
            if assetClass == AssetClassEnum.CRYPTO.value:
                if order.side == OrderDirection.BUY.value:
                    qty = self._RiskManager.calculate_crypto_trade_size(moneyatrisk,(float(order.price)-float(order.stopLoss)))
                if order.side == OrderDirection.SELL.value:
                    qty = self._RiskManager.calculate_crypto_trade_size(moneyatrisk,(float(order.stopLoss)-float(order.price)))
        return self._RiskManager.round_down(abs(qty*order.riskPercentage))

    def _calculateQtyLimit(self, assetClass:str, order:Order)->float:
        moneyatrisk = self._RiskManager.calculate_money_at_risk()
        order.moneyAtRisk = moneyatrisk
        qty = 0.00
        if order.orderType == OrderTypeEnum.LIMIT.value:
            if assetClass == AssetClassEnum.CRYPTO:
                if order.side == OrderDirection.BUY.value:
                    qty = (self._RiskManager.calculate_crypto_trade_size
                           (moneyatrisk, abs(float(order.price) - float(order.slLimitPrice))))
                if order.side == OrderDirection.SELL.value:
                    qty = (self._RiskManager.calculate_crypto_trade_size
                           (moneyatrisk, abs(float(order.slLimitPrice) - float(order.price))))
        return self._RiskManager.round_down(abs(qty))
    # endregion

    # region Functions
    def returnAllTrades(self)->list[Trade]:
        return [trade for trade in self.openTrades.values()]

    def returnTradesForRelation(self,assetBrokerStrategyRelation: AssetBrokerStrategyRelation)->list[Trade]:
        return [x for x in self.openTrades.values() if x.relation.compare(assetBrokerStrategyRelation)]
    # endregion

tm = TradeManager()
order = Order()
order.orderLinkId = str(uuid.uuid4())
order.category = "linear"
order.symbol = "BTCUSDT"
order.price = str(98000)
order.stopLoss = str(99000)
order.riskPercentage = 0.40
order.side = OrderDirection.BUY.value
order.orderType = OrderTypeEnum.MARKET.value

relation = AssetBrokerStrategyRelation("ABC","BYBIT","ABC",1)

order2 = Order()
order2.orderLinkId = str(uuid.uuid4())
order2.category = "linear"
order2.symbol = "BTCUSDT"
order2.price = str(98000)
order2.stopLoss = str(99000)
order2.takeProfit = str(111000)
order2.riskPercentage = 0.25

order2.side = OrderDirection.BUY.value
order2.orderType = OrderTypeEnum.MARKET.value

order3 = Order()
order3.orderLinkId = str(uuid.uuid4())
order3.category = "linear"
order3.symbol = "XRPUSDT"
order3.price = str(2.41)
order3.stopLoss = str(2)
order3.takeProfit = str(3)
order3.riskPercentage = 0.25

order3.side = OrderDirection.BUY.value
order3.orderType = OrderTypeEnum.MARKET.value

trade = Trade(relation,[order])
trade.orders.append(order2)
trade.orders.append(order3)
tm.registerTrade(trade)
tm.placeTrade(trade,"Crypto")
