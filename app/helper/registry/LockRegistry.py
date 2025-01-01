import threading


class LockRegistry:
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
