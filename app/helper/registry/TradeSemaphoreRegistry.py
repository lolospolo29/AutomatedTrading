import threading

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation


class TradeSemaphoreRegistry:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TradeSemaphoreRegistry, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self): # maxtradesperrelation fix
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.registry:dict[AssetBrokerStrategyRelation,threading.Semaphore] = {}  # Map: Relation -> Semaphore
            self._initialized = True

    def register_relation(self, relation:AssetBrokerStrategyRelation):
        """Eine neue Relation registrieren."""
        with self._lock:
            if relation not in self.registry:
                # Erstelle Semaphore mit der maximal erlaubten Anzahl von Trades
                self.registry[relation] = threading.Semaphore(relation.max_trades)

    def acquire_trade(self, relation:AssetBrokerStrategyRelation):
        """Einen Trade für die gegebene Relation starten."""
        with self._lock:
            if relation not in self.registry:
                self.register_relation(relation)  # Automatische Registrierung
            semaphore:threading.Semaphore = self.registry[relation]
        # Versuche, einen Platz für die Relation zu belegen
        acquired = semaphore.acquire() # put in queue
        if not acquired:
            raise ValueError(f"Maximale Anzahl von Trades für Relation {relation} erreicht!")

    def release_trade(self, relation:AssetBrokerStrategyRelation):
        """Einen Trade für die gegebene Relation beenden."""
        with self._lock:
            if relation not in self.registry:
                raise ValueError(f"Relation {relation} nicht registriert!")
            semaphore = self.registry[relation]
        # Gebe einen Platz frei
        semaphore.release()
