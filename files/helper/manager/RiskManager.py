import threading


class RiskManager:
    """
    Manages risk parameters and controls drawdowns for trading accounts.

    A singleton class designed to manage and calculate risk for financial
    transactions or trading systems. The RiskManager allows for setting
    maximum drawdowns, risk percentages, and calculates the amount at
    risk based on the current account balance to ensure disciplined
    risk management.

    :ivar _instance: Singleton instance of the class.
    :type _instance: RiskManager
    :ivar _lock: Lock object to ensure thread-safe instantiation.
    :type _lock: threading.Lock
    :ivar __max_drawdown: The maximum drawdown percentage allowed.
    :type __max_drawdown: float
    :ivar __current_pnl: The current profit and loss value used to track
        drawdown.
    :type __current_pnl: float
    :ivar __max_risk_percentage: The maximum risk percentage allowed based
        on account balance.
    :type __max_risk_percentage: float
    :ivar __account_balance: The current account balance for risk calculation.
    :type __account_balance: float
    :ivar _initialized: Flag indicating whether the instance has been initialized.
    :type _initialized: bool
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RiskManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, max_drawdown: float = 1.0, max_risk_percentage: float = 0.5):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.__max_drawdown: float = max_drawdown  # Maximaler Verlust in %
            self.__current_pnl: float = 0.0  # Aktueller Drawdown
            self.__max_risk_percentage: float = max_risk_percentage
            self.__account_balance = 1000
            self._initialized = True  # Markiere als initialisiert

    @staticmethod
    def breakeven_exchange_rate(current_exchange_rate: float, lower_yield: float, higher_yield: float) -> float:
        """
        Calculates the breakeven exchange rate where the yield advantage of the higher-yielding currency
        is fully offset by exchange rate movement.

        :param current_exchange_rate: Current exchange rate (e.g., EUR/USD = 1.1000)
        :param lower_yield: Yield (interest rate) of the lower-yielding currency (as a decimal, e.g., 0.02 for 2%)
        :param higher_yield: Yield (interest rate) of the higher-yielding currency (as a decimal, e.g., 0.04 for 4%)
        :return: Breakeven exchange rate
        """
        return current_exchange_rate * ((1 + lower_yield) / (1 + higher_yield))

    # # Example usage:
    # current_rate = 1.1000  # EUR/USD
    # lower_yield = 0.01  # EUR at 1%
    # higher_yield = 0.04  # USD at 4%
    #
    # breakeven_rate = breakeven_exchange_rate(current_rate, lower_yield, higher_yield)
    # print(f"Breakeven Exchange Rate: {breakeven_rate:.4f}")

    @property
    def max_risk_percentage(self):
        return self.__max_risk_percentage

    @property
    def account_balance(self):
        return self.__account_balance

    def return_current_pnl(self) -> float:
        return self.__current_pnl

    def add_to_current_pnl(self, pnl: float) -> None:
        self.__current_pnl += pnl

    def calculate_money_at_risk(self):
        """
        Calculates money at risk based on account balance and risk percentage.
        """
        return self.__account_balance * (self.__max_risk_percentage / 100)

    # endregion
