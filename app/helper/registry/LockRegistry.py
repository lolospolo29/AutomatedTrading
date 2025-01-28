import threading


class LockRegistry:
    """
    Responsible for managing a registry of locks. Implements a singleton pattern
    to ensure a single instance manages all lock registrations. Each lock is
    identified by a unique key, allowing for thread-safe operations within a
    multithreaded application. This ensures consistency and provides mechanisms
    to avoid race conditions within the scope of lock management.

    The class maintains its singleton nature via a private static instance and
    uses a thread lock to manage instantiation as well as access to the internal
    dictionary of locks.

    :ivar _instance: Static instance of the singleton LockRegistry class.
    :type _instance: LockRegistry
    :ivar _lock: A lock to ensure thread-safe creation of the singleton instance.
    :type _lock: threading.Lock
    :ivar locks: A dictionary containing thread locks with unique keys.
    :type locks: dict
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(LockRegistry, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.locks = {}
            self._initialized = True

    def get_lock(self, id: str):
        with self._lock:
            if id not in self.locks:
                self.locks[id] = threading.Lock()
            return self.locks[id]
