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

    def __init__(self, maxDrawdown:float = 1.0,maxRiskPercentage:float = 0.25):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.maxDrawdown: float = maxDrawdown  # Maximaler Verlust in %
            self.currentDrawdown: float = 0.0  # Aktueller Drawdown
            self.maxRiskPercentage: float = maxRiskPercentage
            self._initialized = True  # Markiere als initialisiert


    def returnCurrentDrawdown(self) -> float:
        return self.currentDrawdown

    def calculateCurrentDrawdownFromClosedPnl(self,closedPnl: list[float]) -> None:
        for pnl in closedPnl:
            self.currentDrawdown += pnl

    @staticmethod
    def setNewsTime(time):
        return None

    def calculate_money_at_risk(self,account_balance):
        """
        Calculates money at risk based on account balance and risk percentage.
        """
        return account_balance * (self.maxRiskPercentage / 100)

    @staticmethod
    def calculate_crypto_trade_size(money_at_risk, stop_loss_distance):
        """
        Calculates trade size for cryptocurrencies.
        Formula: Trade Size (Units) = Money at Risk / Stop Loss Distance
        """
        return money_at_risk / stop_loss_distance

    @staticmethod
    def calculate_indices_commodities_trade_size(money_at_risk, stop_loss_points, value_per_point):
        """
        Calculates trade size for indices and commodities.
        Formula: Trade Size (Contracts) = Money at Risk / (Stop Loss Points * Value per Point)
        """
        return money_at_risk / (stop_loss_points * value_per_point)

    @staticmethod
    def calculate_forex_trade_size_non_jpy(money_at_risk, stop_loss_pips, pip_value):
        """
        Calculates trade size for non-JPY Forex pairs.
        Formula: Trade Size (Units) = Money at Risk / (Stop Loss in Pips * Pip Value)
        """
        return money_at_risk / (stop_loss_pips * pip_value)

    @staticmethod
    def calculate_forex_trade_size_jpy(money_at_risk, stop_loss_pips, exchange_rate):
        """
        Calculates trade size for JPY Forex pairs.
        Formula: Trade Size (Units) = Money at Risk / (Stop Loss Pips * Pip Value)
        Pip value is adjusted due to how JPY pairs are priced.
        """
        pip_value = 0.01 / exchange_rate  # Adjusted pip value for JPY pairs
        return money_at_risk / (stop_loss_pips * pip_value)

#
# # Input variables
# account_balance = 10000  # Your account balance in USD
# risk_percentage = 2  # Risk percentage
#
# # Example 1: Cryptocurrency example
# crypto_open_price = 100649.11000
# crypto_close_price = 98636.12780
# crypto_stop_loss_distance = crypto_open_price - crypto_close_price  # Distance in price
# money_at_risk = calculate_money_at_risk(account_balance, risk_percentage)
# crypto_trade_size = calculate_crypto_trade_size(money_at_risk, crypto_stop_loss_distance)
#
# # Example 2: Indices/Commodities example
# stop_loss_points = 20  # Example stop loss distance in points
# value_per_point = 10  # Example $10 per point (typical for indices/commodities)
# indices_commodities_trade_size = calculate_indices_commodities_trade_size(
#     money_at_risk, stop_loss_points, value_per_point
# )
#
# # Example 3: Forex Non-JPY
# stop_loss_pips_non_jpy = 50  # Example stop loss of 50 pips
# pip_value_non_jpy = 0.0001  # Pip value for non-JPY pairs
# forex_non_jpy_trade_size = calculate_forex_trade_size_non_jpy(
#     money_at_risk, stop_loss_pips_non_jpy, pip_value_non_jpy
# )
#
# # Example 4: Forex JPY
# stop_loss_pips_jpy = 50  # Example stop loss of 50 pips
# exchange_rate_jpy = 120  # Example exchange rate for USD/JPY
# forex_jpy_trade_size = calculate_forex_trade_size_jpy(
#     money_at_risk, stop_loss_pips_jpy, exchange_rate_jpy
# )

