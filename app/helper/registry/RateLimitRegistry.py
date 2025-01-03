import threading
from threading import Semaphore
from functools import wraps


class RateLimitRegistry:

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

#Threading Example
#
# @rate_limit_registry.rate_limited
# def returnTickers(category, symbol=None, baseCoin=None, expDate=None)->bool:
#     print(f"Fetching tickers for category {category}, symbol {symbol}, baseCoin {baseCoin}, expDate {expDate}")
#     # Simulated workload
#     import time
#     time.sleep(1)
#     return True
#
#
# @rate_limit_registry.rate_limited
# def anotherFunction():
#     print("Executing another function")
#     # Simulated workload
#     import time
#     time.sleep(1)
#
#
# # Test the functionality
# if __name__ == "__main__":
#     import threading
#
#
#     def test_function():
#         try:
#             returnTickers("CategoryA", "BTC", "USD")
#         except ValueError as e:
#             print(e)
#
#
#     threads = [threading.Thread(target=test_function) for _ in range(7)]
#
#     for t in threads:
#         t.start()
#     for t in threads:
#         t.join()
