import queue
import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.models.frameworks.FrameWork import FrameWork


class Order:
    # Required parameters
    status: bool

    entryFrameWork: FrameWork
    confirmations: list[FrameWork]
    logFile: str

    createdAt: datetime
    openedAt: datetime
    closedAt: datetime
    updatedAt: datetime

    riskPercentage: float
    moneyAtRisk: float
    leverage: float
    unrealisedPnL: float
    price: str

    orderLinkId: str
    orderType:str

    symbol: str
    category: str
    side: str
    takeProfit: str
    stopLoss: str
    qty: str

    # Must be set after sending Request
    orderId: str

    # Spot Logic
    isLeverage: int
    marketUnit: str
    orderFilter: str
    orderlv: str

    # Specific attributes (optional)
    timeInForce: str
    closeOnTrigger: bool
    reduceOnly: bool
    tpOrderType: str
    slOrderType: str
    triggerDirection: int
    tpTriggerBy: str
    slTriggerBy: str

    # Limit Logic attributes (optional)
    tpslMode: str
    orderPrice: str
    triggerPrice: str
    tpLimitPrice: str
    slLimitPrice: str

    def __init__(self):
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._priority_queue = queue.PriorityQueue()
        self._current_thread = None
        self.createdAt = datetime.now()

    def acquire(self, priority, thread_name):
        with self._lock:
            self._priority_queue.put((priority, thread_name))
            print(f"{thread_name} mit Priorität {priority} wartet.")

            while self._priority_queue.queue[0][1] != thread_name or self._current_thread is not None:
                self._condition.wait()

            self._priority_queue.get()
            self._current_thread = thread_name
            print(f"{thread_name} hat den Lock übernommen.")

    def release(self, thread_name):
        with self._lock:
            if self._current_thread == thread_name:
                print(f"{thread_name} gibt den Lock frei.")
                self._current_thread = None
                self._condition.notify_all()

    def __setattr__(self, key, value):
        # Update updatedAt whenever an attribute is changed
        super().__setattr__(key, value)
        if key != 'updatedAt':  # Avoid recursive updates
            super().__setattr__('updatedAt', datetime.now())

    def __getattribute__(self, key):
        if key != 'updatedAt':
            object.__setattr__(self, 'updatedAt', datetime.now())
        return super().__getattribute__(key)


