import threading

from logging import Logger

from files.helper.mediator.PriceMediator import PriceMediator
from files.models.asset.Candle import Candle
from files.models.asset.Relation import Relation

#todo class instance
class PriceMediatorRegistry:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super(PriceMediatorRegistry, cls).__new__(cls)
        return cls._instance

    # region Initializing

    def __init__(self,logger: Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self._price_mediators:dict[str,PriceMediator] = {}
            self._logger = logger
            self._initialized = True

    def register_mediator(self, relation:Relation, price_mediator:PriceMediator):
        if relation.asset + relation.broker not in self._price_mediators:
            self._price_mediators[relation.asset+relation.broker] = price_mediator
            self._logger.info(f"Price Mediator for {relation.asset} + {relation.broker} registered")

    def delete_mediator(self, relation: Relation):
        try:
            if relation.asset + relation.broker in self._price_mediators:
                del self._price_mediators[relation.asset+relation.broker]
                self._logger.info(f"Price Mediator for {relation.asset} + {relation.broker} deleted")
        except Exception as e:
            self._logger.exception(f"Price Mediator for {relation.asset} + {relation.broker} deletion failed: {e}")

    def get_mediator(self, relation: Relation) -> PriceMediator:
        try:
            if relation.asset + relation.broker in self._price_mediators:
                return self._price_mediators[relation.asset+relation.broker]
        except Exception as e:
            self._logger.exception(f"{relation.asset} + {relation.broker} retrieval failed: {e}")

    def analyze_mediator(self, relation: Relation, candles:list[Candle], timeframe:int):
        try:
            if relation.asset + relation.broker in self._price_mediators and len(candles) >= 3:
                mediator = self._price_mediators[relation.asset+relation.broker]
                mediator.analyze(first_candle=candles[-3], second_candle=candles[-2], third_candle=candles[-1], timeframe=timeframe)
        except Exception as e:
            self._logger.exception(f"Price Mediator :{relation.asset} + {relation.broker} analysis failed: {e}")