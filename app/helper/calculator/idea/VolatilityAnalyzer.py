import numpy as np

from app.helper.manager.RiskManager import RiskManager


class VolatilityAnalyzer:
    """ATR (Average True Range) for price-based volatility.
        Historical volatility using standard deviation of returns.
        Pip values, tick values, and point values dynamically for different assets.
        Portfolio-wide volatility assessment for risk-adjusted position sizing"""

    def __init__(self):
        self._risk_manager = RiskManager()
        self._asset_atr: dict[str, float] = {}
        self._asset_last_candle_close: dict[str, float] = {}

    def add_atr(self, asset: str, atr: float):
        self._asset_atr[asset] = atr

    def add_last_candle_close(self, asset: str, last_candle_close: float):
        self._asset_last_candle_close[asset] = last_candle_close

    def get_crypto_volatility(self, asset: str, lookback: int = 14) -> float:
        """
        Calculates ATR (Average True Range) as a proxy for cryptocurrency volatility.

        :param asset: The cryptocurrency symbol (e.g., "BTC/USD").
        :param lookback: Number of periods to consider for ATR calculation.
        :return: Volatility factor based on ATR.
        """
        return self._asset_atr[asset] / self._asset_last_candle_close[asset]

    def get_forex_volatility(self, pair: str, lookback: int = 14) -> float:
        """
        Calculates historical volatility for a Forex pair.

        :param pair: The Forex pair (e.g., "EUR/USD").
        :param lookback: Number of periods for standard deviation calculation.
        :return: Forex volatility percentage.
        """

        return (self._asset_atr[pair] / self._asset_last_candle_close[pair]) * 100

    def get_pip_value(self, pair: str, lot_size: int = 100000) -> float:
        """
        Calculates pip value dynamically based on currency pair.

        :param pair: The Forex pair (e.g., "EUR/USD").
        :param lot_size: Standard lot size (default: 100,000).
        :return: Pip value in quote currency.
        """
        price = self._asset_last_candle_close[pair]

        if "JPY" in pair:
            pip_value = (lot_size * 0.01) / price  # JPY pairs have 2 decimal places
        else:
            pip_value = (lot_size * 0.0001) / price  # Non-JPY pairs have 4 decimal places

        return pip_value

    def get_index_point_value(self, index: str) -> float:
        """
        Retrieves the value per point for indices.

        :param index: Index symbol (e.g., "SP500", "DAX").
        :return: Point value.
        """
        point_values = {
            "SP500": 50,  # S&P 500 futures
            "DAX": 25,    # DAX futures
            "NASDAQ": 20,
            "FTSE": 10
        }
        return point_values.get(index, 50)  # Default to 50 if unknown

    def get_commodity_specs(self, commodity: str):
        """
        Retrieves contract size and tick size for commodities.

        :param commodity: The commodity symbol (e.g., "GOLD", "OIL").
        :return: (Contract size, Tick size).
        """
        commodity_data = {
            "XAUUSD": (100, 0.10),  # 100 oz per contract, $0.10 tick
            "OIL": (1000, 0.01),  # 1000 barrels, $0.01 tick
            "SILVER": (5000, 0.005)
        }
        return commodity_data.get(commodity, (100, 0.10))  # Default to GOLD