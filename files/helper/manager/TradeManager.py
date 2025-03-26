import threading
from logging import Logger

from files.db.repositories.TradeRepository import TradeRepository
from files.helper.registry.LockRegistry import LockRegistry
from files.models.trade.Broker import Broker
from files.models.trade.Order import Order
from files.models.trade.Trade import Trade

class TradeManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(TradeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, trade_repository:TradeRepository,logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._lock_registry = LockRegistry()
            self._open_trades: dict[str, Trade] = {}
            self._orders: dict[str, list[Order]] = {}
            self._trade_repository: TradeRepository = trade_repository
            self._logger = logger
            self._initialized = True  # Markiere als initialisiert

    def create_trade(self, trade: Trade):
        if trade.trade_id in self._open_trades:
            self._logger.info(f"Write Trade To DB,TradeId: {trade.trade_id}")
            self._trade_repository.add_trade(trade)
            self.add_trade(trade)

    def create_order(self, order: Order):
        if order.trade_id not in self._open_trades[order.tradeId]:
            self._logger.info(
                f"Write Order To DB,OrderLinkId: {order.order_link_id},TradeId:{order.tradeId},Symbol:{order.symbol}")
            self._trade_repository.add_order(order)
            self.add_order(order)

    def add_trade(self, trade: Trade):
        tradeLock = self._lock_registry.get_lock(trade.trade_id)
        with tradeLock:
            if trade.trade_id not in self._open_trades:
                self._open_trades[trade.trade_id] = trade
                self._logger.info(f"Register Trade,TradeId: {trade.trade_id}")

    def add_order(self, order: Order):
        orderLock = self._lock_registry.get_lock(order.order_link_id)
        with orderLock:
            self._orders[order.trade_id].append(order)
            self._logger.info(f"Register Order,OrderId: {order.order_link_id},TradeId:{order.trade_id}")

    def get_trades(self)->list[Trade]:
        return self._trade_repository.get_trades()

    def get_brokers(self)->list[Broker]:
        return self._trade_repository.find_brokers()

    def get_trades_for_relation(self, relation_id:str) -> list[Trade]:
        trades = []
        for id, trade in self._open_trades.items():
            try:
                if trade.relation_id == relation_id:
                    trades.append(trade)
            except AttributeError as e:
                self._logger.error("Return Trades Error,Error:{e}".format(e=e))
        return trades

    def get_orders_for_relation(self, trade_id:str) -> list[Order]:
        orders = []
        for id, order in self._orders.items():
            if trade_id in order:
                orders.append(order)
        return orders

    def update_trade(self, trade: Trade):
        tradeLock = self._lock_registry.get_lock(trade.trade_id)
        with tradeLock:
            self._logger.info(f"Update To DB,TradeId: {trade.trade_id}")
            self._trade_repository.update_trade(trade)

    def update_order(self, order: Order):
        orderLock = self._lock_registry.get_lock(order.order_link_id)
        with orderLock:
            self._logger.info(f"Update Order in DB,OrderLinkId: {order.order_link_id},TradeId:{order.tradeId},Symbol:{order.symbol}")
            orderLock = self._lock_registry.get_lock(order.order_link_id)
            with orderLock:
                self._trade_repository.update_order(order)

    def remove_order(self, order: Order):
        orders = self._orders[order.trade_id]
        for order in orders:
            if order.order_link_id == order.order_link_id:
                orders.remove(order)
                return

    def remove_trade(self, trade: Trade):
        try:
            if trade.trade_id in self._open_trades:
                del self._open_trades[trade.trade_id]
                self._logger.info(f"Remove Trade,TradeId: {trade.trade_id}")
        except AttributeError as e:
            self._logger.fatal(f"Remove Trade Error,TradeId: {trade.trade_id}: {e}")