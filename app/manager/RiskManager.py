import math
import threading

from app.models.asset.AssetClassEnum import AssetClassEnum
from app.models.trade.Order import Order
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class RiskManager:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RiskManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, max_drawdown:float = 1.0, max_risk_percentage:float = 0.5):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.__max_drawdown: float = max_drawdown  # Maximaler Verlust in %
            self.__current_pnl: float = 0.0  # Aktueller Drawdown
            self.__max_risk_percentage: float = max_risk_percentage
            self.__account_balance = 1000
            self._initialized = True  # Markiere als initialisiert

    def return_current_pnl(self) -> float:
        return self.__current_pnl

    def set_current_pnl(self, pnl: float) -> None:
        self.__current_pnl += pnl

    def _calculate_money_at_risk(self):
        """
        Calculates money at risk based on account balance and risk percentage.
        """
        return self.__account_balance * (self.__max_risk_percentage / 100)

    @staticmethod
    def _calculate_crypto_trade_size(money_at_risk, stop_loss_distance):
        """
        Calculates trade size for cryptocurrencies.
        Formula: Trade Size (Units) = Money at Risk / Stop Loss Distance
        """
        return money_at_risk / stop_loss_distance

    @staticmethod
    def _calculate_indices_commodities_trade_size(money_at_risk, stop_loss_points, value_per_point=100):
        """
        Calculates trade size for indices and commodities.
        Formula: Trade Size (Contracts) = Money at Risk / (Stop Loss Points * Value per Point)
        """
        return money_at_risk / (stop_loss_points * value_per_point)

    @staticmethod
    def _calculate_forex_trade_size_non_jpy(money_at_risk, stop_loss_pips, pip_value=1):
        """
        Calculates trade size for non-JPY Forex pairs.
        Formula: Trade Size (Units) = Money at Risk / (Stop Loss in Pips * Pip Value)
        """
        return money_at_risk / (stop_loss_pips * pip_value)

    @staticmethod
    def _calculate_forex_trade_size_jpy(money_at_risk, stop_loss_pips, exchange_rate=0.01):
        """
        Calculates trade size for JPY Forex pairs.
        Formula: Trade Size (Units) = Money at Risk / (Stop Loss Pips * Pip Value)
        Pip value is adjusted due to how JPY pairs are priced.
        """
        pip_value = 0.01 / exchange_rate  # Adjusted pip value for JPY pairs
        return money_at_risk / (stop_loss_pips * pip_value)

    @staticmethod
    def _round_down(value: float) -> float:
        """
        Rundet einen Wert immer auf die nächste niedrigere Stelle ab.

        :param value: Der Eingabewert (float).
        :return: Abgerundeter Wert (float).
        """
        if value == 0:
            return 0  # Spezieller Fall, wenn der Wert 0 ist
        factor = 10 ** math.floor(math.log10(abs(value)))
        return math.floor(value / factor) * factor

    # region Risk Management
    def calculate_qty_market(self, asset_class:str, order:Order)->float:
        try:
            moneyatrisk = self._calculate_money_at_risk()
            order.money_at_risk = moneyatrisk
            qty = 0.00
            if asset_class == AssetClassEnum.CRYPTO.value:
                if order.side == OrderDirectionEnum.BUY.value:
                    qty = self._calculate_crypto_trade_size(moneyatrisk,
                                                                         (float(order.price) - float(order.stopLoss)))
                if order.side == OrderDirectionEnum.SELL.value:
                    qty = self._calculate_crypto_trade_size(moneyatrisk,
                                                                         (float(order.stopLoss) - float(order.price)))

            return self._round_down(abs(qty * order.risk_percentage))
        except Exception as e:
            logger.exception("Failed to Calculate Qty Market.")

    def calculate_qty_limit(self, asset_class:str, order:Order)->float:
        try:
            moneyatrisk = self._calculate_money_at_risk()
            order.money_at_risk = moneyatrisk
            qty = 0.00
            if asset_class == AssetClassEnum.CRYPTO:
                if order.side == OrderDirectionEnum.BUY.value:
                    qty = (self._calculate_crypto_trade_size
                           (moneyatrisk, abs(float(order.price) - float(order.slLimitPrice))))
                if order.side == OrderDirectionEnum.SELL.value:
                    qty = (self._calculate_crypto_trade_size
                           (moneyatrisk, abs(float(order.slLimitPrice) - float(order.price))))
            return self._round_down(abs(qty * order.risk_percentage))
        except Exception as e:
            logger.exception("Failed to Calculate Qty Limit.")
    # endregion
# #
# # # Input variables
# rm = RiskManager()
# account_balance = 1000  # Your account balance in USD
#
# # Example 1: Cryptocurrency example
# crypto_open_price = 98000
# crypto_close_price = 97000
# crypto_stop_loss_distance = crypto_open_price - crypto_close_price  # Distance in price
# money_at_risk = rm._calculate_money_at_risk(account_balance)
# print(money_at_risk)
# crypto_trade_size = rm._calculate_crypto_trade_size(money_at_risk, crypto_stop_loss_distance)
# print(crypto_trade_size)
#
# # Example 2: Indices/Commodities example
# stop_loss_points = 10  # Example stop loss distance in points
# value_per_point = 100  # Example $10 per point (typical for indices/commodities)
# indices_commodities_trade_size = rm._calculate_indices_commodities_trade_size(
#     money_at_risk, stop_loss_points, value_per_point
# )
# print(indices_commodities_trade_size)
#
# # Example 3: Forex Non-JPY
# stop_loss_pips_non_jpy = 100  # Example stop loss of 50 pips
# pip_value_non_jpy = 1  # Pip value for non-JPY pairs
# forex_non_jpy_trade_size = rm._calculate_forex_trade_size_non_jpy(
#     money_at_risk, stop_loss_pips_non_jpy, pip_value_non_jpy
# )
# print(forex_non_jpy_trade_size)
# # Example 4: Forex JPY
# stop_loss_pips_jpy = 100
# exchange_rate_jpy = 0.01  # Example exchange rate for USD/JPY
# forex_jpy_trade_size = rm._calculate_forex_trade_size_jpy(
#     money_at_risk, stop_loss_pips_jpy, exchange_rate_jpy
# )
# print(forex_jpy_trade_size)