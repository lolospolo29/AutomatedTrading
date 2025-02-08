import threading

from app.models.asset.Relation import Relation
from app.monitoring.logging.logging_startup import logger


class SemaphoreRegistry:
    """
    A thread-safe registry that manages semaphores for trade limits on different
    asset-broker-strategy relations.

    This class ensures that each AssetBrokerStrategyRelation has its corresponding
    semaphore initialized and managed. This semaphore is used to control the number
    of concurrent trades allowed for the given relation. The registry implements the
    singleton pattern to ensure that only one instance is managing the semaphores
    across the application.

    :ivar _instance: The singleton instance of the registry.
    :type _instance: SemaphoreRegistry
    :ivar _lock: A threading.Lock to ensure thread safety during registry operations.
    :type _lock: threading.Lock
    :ivar registry: A mapping of AssetBrokerStrategyRelation to their corresponding
        threading.Semaphore objects.
    :type registry: dict[Relation, threading.Semaphore]
    :ivar _initialized: A flag indicating whether the instance has been initialized.
    :type _initialized: bool
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SemaphoreRegistry, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self): # maxtradesperrelation fix
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.registry:dict[str,threading.Semaphore] = {}  # Map: Relation -> Semaphore
            self._initialized = True

    def register_relation(self, key:str,max_semaphores:int=1):
        """Eine neue Relation registrieren."""
        with self._lock:
            if key not in self.registry:
                # Erstelle Semaphore mit der maximal erlaubten Anzahl von Trades
                self.registry[key] = threading.Semaphore(max_semaphores)
    def acquire_trade(self,  key:str):
        """Einen Trade für die gegebene Relation starten."""
        with self._lock:
            if key not in self.registry:
                self.register_relation(key)  # Automatische Registrierung
            semaphore:threading.Semaphore = self.registry[key]
        # Versuche, einen Platz für die Relation zu belegen
        acquired = semaphore.acquire() # put in queue
        if not acquired:
            logger.exception("Acquired semaphore was already acquired")

    def release_trade(self, relation:Relation):
        """Einen Trade für die gegebene Relation beenden."""
        with self._lock:
            if relation not in self.registry:
                logger.exception("Acquired semaphore was already acquired")
            semaphore = self.registry[relation]
        # Gebe einen Platz frei
        semaphore.release()
