import math

from files.helper.manager.RiskManager import RiskManager
from files.models.asset.AssetClassEnum import AssetClassEnum

class PositionSizeCalculator:
    def __init__(self):
        self._risk_manager = RiskManager()

    def _calculate_crypto_trade_size(self, entry_price, stop_loss_price):
        """
        Calculates trade size for cryptocurrencies.
        Formula: Trade Size (Units) = Money at Risk / Stop Loss Distance
        """
        # Berechne das Risiko in Dollar
        risk_amount = (self._risk_manager.max_risk_percentage / 100) * self._risk_manager.account_balance

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
        risk_amount = (self._risk_manager.max_risk_percentage / 100) * self._risk_manager.account_balance

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
        risk_amount = (self._risk_manager.max_risk_percentage / 100) * self._risk_manager.account_balance

        # Calculate the pip distance
        pip_distance = abs(entry_price - stop_loss_price) * 10000  # Assumes 4 decimal place pairs like EUR/USD

        # Calculate the position size in lots
        if pip_distance == 0:
            raise ValueError("The entry price and stop-loss price cannot be the same.")

        position_size = risk_amount / (pip_value * pip_distance)
        return position_size

    def _calculate_commodity_position_size(self, entry_price, stop_loss_price, contract_size,
                                           tick_size):
        risk_amount = (self._risk_manager.max_risk_percentage / 100) * self._risk_manager.account_balance

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


    def _calculate_qty_based_on_asset_class(self, asset_class:str, entry_price:float, stop_loss:float, pip_value:int=10,
                                            lot_size:int=100000, point_value:int=50,tick_size:float=0.10,contract_size:int=100) -> float:
        """
        Calculates the trade quantity based on the provided asset class and associated financial parameters.
        The method handles specific asset classes such as cryptocurrency, forex (with or without JPY pairing),
        commodities, and indices. For each asset class, the trade size is calculated using varying financial
        metrics like pip value, lot size, or point value. Depending on the asset class, the required financial
        parameters are applied to their respective trade size computation methods. Returns the calculated
        quantity for the trade.

        :param asset_class: The class of the asset for which the trade quantity is being calculated.
        :param entry_price: The price at which the entry into the trade takes place.
        :param stop_loss: The price at which the stop-loss order is set to manage risk in the trade.
        :param pip_value: (Optional) Value per pip, typically used for forex calculations. Defaults to None.
        :param lot_size: (Optional) Size of the lot, used specifically for Forex JPY pair computations.
        :param point_value: (Optional) Value of a point, typically used for commodity and indices calculations.
        :return: The computed trade quantity based on the asset class and provided parameters.
        """
        qty = 0
        if asset_class == AssetClassEnum.CRYPTO.value:
            qty = self._calculate_crypto_trade_size(float(entry_price), float(stop_loss))
        if asset_class == AssetClassEnum.FX.value:
            if pip_value is None:
                qty = self._calculate_forex_trade_size_non_jpy(float(entry_price), float(stop_loss))
            if pip_value is not None:
                qty = self._calculate_forex_trade_size_non_jpy(float(entry_price), float(stop_loss), pip_value=pip_value)
        if asset_class == AssetClassEnum.FXJPY.value:
            qty = self._calculate_forex_trade_size_jpy(float(entry_price), float(stop_loss),lot_size=lot_size)
        if asset_class == AssetClassEnum.COMMODITY.value:
            qty = self._calculate_commodity_position_size(float(entry_price), float(stop_loss),tick_size=tick_size,contract_size=contract_size)
        if asset_class == AssetClassEnum.INDICE.value:
            qty = self._calculate_indices_trade_size(float(entry_price), float(stop_loss),point_value=point_value)

        return qty

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

    def calculate_order_qty(self, asset_class: str, entry_price:float, exit_price:float, risk_percentage:float=1,
                            pip_value:int=None, lot_size:int=None, point_value:int=None) -> float:
        """
        Calculates the order quantity based on the asset class, entry and exit prices,
        risk percentage, and optional parameters such as pip value, lot size, and point value.
        This method determines the appropriate quantity to trade based on the specified financial
        risk parameters and the nature of the financial instrument.

        :param asset_class: Specifies the type of financial instrument (e.g., forex, stocks, commodities).
        :param entry_price: Entry price for the trade.
        :param exit_price: Exit price for the trade, typically used for stop-loss calculation.
        :param risk_percentage: Percentage of the order risk per trade.
        :param pip_value: Specifies pip value, applicable for forex instruments.
        :param lot_size: Lot size applicable to the type of financial instrument.
        :param point_value: Specifies point value for instruments like indices or futures.
        :return: The calculated order quantity as a float value.
        """
        qty = self._calculate_qty_based_on_asset_class(asset_class=asset_class, entry_price=entry_price
                                                       , stop_loss=exit_price
                                                       , pip_value=pip_value, lot_size=lot_size, point_value=point_value)
        return self._round_down(abs(qty*risk_percentage))