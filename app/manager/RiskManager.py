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

    def __init__(self, max_drawdown: float = 1.0, max_risk_percentage: float = 0.5):
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

    def _calculate_crypto_trade_size(self, entry_price, stop_loss_price):
        """
        Calculates trade size for cryptocurrencies.
        Formula: Trade Size (Units) = Money at Risk / Stop Loss Distance
        """
        # Berechne das Risiko in Dollar
        risk_amount = (self.__max_risk_percentage / 100) * self.__account_balance

        # Berechne den Abstand zwischen Entry und Stop-Loss
        distance = abs(entry_price - stop_loss_price)

        if distance == 0:
            raise ValueError("Der Entry-Preis und der Stop-Loss-Preis dürfen nicht gleich sein.")

        # Berechne die Quantity Size
        quantity = risk_amount / distance
        return quantity

    def _calculate_indices_trade_size(self, entry_price, stop_loss_price, point_value=50):
        """
        Calculates trade size for indices and commodities.
        Formula: Trade Size (Contracts) = Money at Risk / (Stop Loss Points * Value per Point)
        """
        # Calculate the risk amount in dollars
        risk_amount = (self.__max_risk_percentage / 100) * self.__account_balance

        # Calculate the point distance
        point_distance = abs(entry_price - stop_loss_price)

        # Ensure no division by zero
        if point_distance == 0:
            raise ValueError("The entry price and stop-loss price cannot be the same.")

        # Calculate the position size
        position_size = risk_amount / (point_value * point_distance)
        return position_size

    def _calculate_forex_trade_size_jpy(self, entry_price, stop_loss_price, lot_size=100000):
        """
        Calculates trade size for non-JPY Forex pairs.
        Formula: Trade Size (Units) = Money at Risk / (Stop Loss in Pips * Pip Value)
        """
        pip_value = (lot_size * 0.01) / entry_price

        return self._calculate_forex_trade_size_non_jpy(entry_price, stop_loss_price, pip_value=pip_value)

    def _calculate_forex_trade_size_non_jpy(self, entry_price, stop_loss_price, pip_value=10):
        """
        Calculates trade size for JPY Forex pairs.
        Formula: Trade Size (Units) = Money at Risk / (Stop Loss Pips * Pip Value)
        Pip value is adjusted due to how JPY pairs are priced.
        """
        # Calculate the risk amount in dollars
        risk_amount = (self.__max_risk_percentage / 100) * self.__account_balance

        # Calculate the pip distance
        pip_distance = abs(entry_price - stop_loss_price) * 10000  # Assumes 4 decimal place pairs like EUR/USD

        # Calculate the position size in lots
        if pip_distance == 0:
            raise ValueError("The entry price and stop-loss price cannot be the same.")

        position_size = risk_amount / (pip_value * pip_distance)
        return position_size

    def _calculate_commodity_position_size(self, entry_price, stop_loss_price, contract_size,
                                          tick_size):
        risk_amount = (self.__max_risk_percentage / 100) * self.__account_balance

        # Calculate the tick value
        tick_value = contract_size * tick_size

        # Calculate the tick distance
        tick_distance = abs(entry_price - stop_loss_price) / tick_size

        # Ensure no division by zero
        if tick_distance == 0:
            raise ValueError("The entry price and stop-loss price cannot be the same.")

        # Calculate the position size
        position_size = risk_amount / (tick_value * tick_distance)
        return position_size

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
    def calculate_qty(self, asset_class: str, order: Order) -> float:
        moneyatrisk = self._calculate_money_at_risk()
        order.money_at_risk = moneyatrisk
        qty = 0.00
        if asset_class == AssetClassEnum.CRYPTO.value:
            qty = self._calculate_crypto_trade_size(float(order.price), float(order.stopLoss))
        if asset_class == AssetClassEnum.FX.value:
            qty = self._calculate_forex_trade_size_non_jpy(float(order.price), float(order.stopLoss))
        if asset_class == AssetClassEnum.FXJPY.value:
            qty = self._calculate_forex_trade_size_jpy(float(order.price), float(order.stopLoss))
        if asset_class == AssetClassEnum.COMMODITY.value:
            qty = self._calculate_indices_trade_size(float(order.price), float(order.stopLoss))


        return self._round_down(abs(qty * order.risk_percentage))

    # endregion
