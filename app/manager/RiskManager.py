import threading


class RiskManager:
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

    @property
    def max_risk_percentage(self):
        return self.__max_risk_percentage

    @property
    def account_balance(self):
        return self.__account_balance

    def return_current_pnl(self) -> float:
        return self.__current_pnl

    def set_current_pnl(self, pnl: float) -> None:
        self.__current_pnl += pnl

    def calculate_money_at_risk(self):
        """
        Calculates money at risk based on account balance and risk percentage.
        """
        return self.__account_balance * (self.__max_risk_percentage / 100)

    # endregion
