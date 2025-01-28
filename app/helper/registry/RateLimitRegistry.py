import threading
from threading import Semaphore
from functools import wraps


class RateLimitRegistry:
    """
    Manages rate limiting using semaphores for functions based on provided enums.

    The `RateLimitRegistry` class is designed as a singleton to maintain a registry
    of semaphores for rate limiting functionality. It ensures that semaphores are
    created and managed uniquely for a given set of enumerated values and are used
    to throttle function execution. This helps in applying rate limits to specific
    functions environments where concurrent calls are controlled.

    :ivar _instances: Dictionary storing singleton instances for each `rate_limit_enum`.
                       It ensures one instance per enum, maintaining thread safety.
    :type _instances: dict
    :ivar _lock: Threading lock to manage concurrent access and ensure thread-safe
                 creation of instances.
    :type _lock: threading.Lock
    """
    _instances = {}  # Store instances for different rate_limit_enum classes
    _lock = threading.Lock()  # Lock for thread safety

    def __new__(cls, rate_limit_enum, *args, **kwargs):
        """
        Create a singleton instance for each rate_limit_enum class.
        """
        # Check if we already have an instance for the specific enum
        if rate_limit_enum not in cls._instances:
            with cls._lock:
                if rate_limit_enum not in cls._instances:
                    # Create a new instance for the enum
                    instance = super(RateLimitRegistry, cls).__new__(cls, *args, **kwargs)
                    cls._instances[rate_limit_enum] = instance
        return cls._instances[rate_limit_enum]

    def __init__(self, rate_limit_enum):
        """
        Initializes the rate limit registry with semaphores for the provided enum.
        Ensures that semaphores are only initialized once.
        """
        if not hasattr(self, "_initialized"):  # Prevent reinitialization
            self._initialized = True
            # Initialize semaphores only for the provided enum values
            self._semaphores = {
                name: Semaphore(limit.value) for name, limit in rate_limit_enum.__members__.items()
            }

    def get_semaphore(self, func_name):
        return self._semaphores.get(func_name)

    def rate_limited(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            semaphore = self.get_semaphore(func_name)
            if not semaphore:
                raise ValueError(f"No semaphore registered for function {func_name}")

            with semaphore:
                return func(*args, **kwargs)

        return wrapper
