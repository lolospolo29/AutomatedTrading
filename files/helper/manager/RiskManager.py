import threading
from logging import Logger

# todo risk manager risk profile crud
# todo risk manager update drawdown after trade / get balance from broker / split up by asset_class

class RiskManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RiskManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, max_drawdown:float, max_risk_percentage: float,logger:Logger):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.__max_drawdown: float = max_drawdown  # Maximaler Verlust in %
            self.__current_pnl: float = 0.0  # Aktueller Drawdown
            self.__max_risk_percentage: float = max_risk_percentage
            self.__account_balance = 1000
            self._logger = logger
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
