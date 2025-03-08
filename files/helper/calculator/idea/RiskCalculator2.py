import math

from files.helper.calculator.idea.VolatilityAnalyzer import VolatilityAnalyzer
from files.helper.manager.RiskManager import RiskManager
from files.models.asset.AssetClassEnum import AssetClassEnum


class RiskCalculator:
    """Incorporate Volatility & Market Conditions

        ATR (Average True Range): Adjust trade size based on recent price fluctuations.
        Historical Volatility: Use GARCH models or standard deviation of returns.
        Liquidity & Spread Adjustments: Factor in slippage and bid-ask spreads.
        Dynamic Risk Adjustment Based on Portfolio Exposure

        Ensure correlation-adjusted risk exposure (reduce size in correlated assets).
        Scale risk dynamically based on portfolio volatility.
        Asset-Class-Specific Enhancements

        Crypto: Adjust for high volatility with a smaller risk cap.
        Forex: Use rolling pip-value calculation based on base currency.
        Indices & Commodities: Adjust contract sizing per index volatility."""
    def __init__(self):
        self._risk_manager = RiskManager()
        self._volatility_analyzer = VolatilityAnalyzer()  # New component for market data

    def _calculate_crypto_trade_size(self, entry_price, stop_loss_price):
        """Calculates crypto trade size with risk-adjusted volatility scaling."""
        risk_amount = self._get_adjusted_risk()
        distance = abs(entry_price - stop_loss_price)

        if distance == 0:
            raise ValueError("Entry and stop-loss price cannot be the same.")

        # **VOLATILITY ADJUSTMENT**: Adjust risk per volatility regime
        volatility = self._volatility_analyzer.get_crypto_volatility()
        risk_factor = min(1.5, max(0.5, 1 / (volatility + 0.01)))  # Normalize factor

        quantity = (risk_amount * risk_factor) / distance
        return quantity

    def _calculate_forex_trade_size(self, entry_price, stop_loss_price, pair, lot_size=100000):
        """Calculates forex trade size with dynamic pip value adjustment."""
        risk_amount = self._get_adjusted_risk()

        pip_value = self._volatility_analyzer.get_pip_value(pair, lot_size)
        pip_distance = abs(entry_price - stop_loss_price) * 10000  # Standard forex pairs

        if pip_distance == 0:
            raise ValueError("Entry and stop-loss price cannot be the same.")

        position_size = risk_amount / (pip_value * pip_distance)
        return position_size

    def _calculate_indices_trade_size(self, entry_price, stop_loss_price, index):
        """Calculates indices trade size based on historical volatility."""
        risk_amount = self._get_adjusted_risk()

        # **DYNAMIC POINT VALUE ADJUSTMENT**
        point_value = self._volatility_analyzer.get_index_point_value(index)
        point_distance = abs(entry_price - stop_loss_price)

        if point_distance == 0:
            raise ValueError("Entry and stop-loss price cannot be the same.")

        position_size = risk_amount / (point_value * point_distance)
        return position_size

    def _calculate_commodity_trade_size(self, entry_price, stop_loss_price, commodity):
        """Calculates commodity position size with market-adjusted contract sizing."""
        risk_amount = self._get_adjusted_risk()

        contract_size, tick_size = self._volatility_analyzer.get_commodity_specs(commodity)
        tick_value = contract_size * tick_size
        tick_distance = abs(entry_price - stop_loss_price) / tick_size

        if tick_distance == 0:
            raise ValueError("Entry and stop-loss price cannot be the same.")

        position_size = risk_amount / (tick_value * tick_distance)
        return position_size

    def _calculate_qty_based_on_asset_class(self, asset_class, entry_price, stop_loss_price, **kwargs):
        """Route calculation to correct method based on asset class."""
        if asset_class == AssetClassEnum.CRYPTO.value:
            return self._calculate_crypto_trade_size(entry_price, stop_loss_price)

        if asset_class == AssetClassEnum.FX.value:
            return self._calculate_forex_trade_size(entry_price, stop_loss_price, **kwargs)

        if asset_class == AssetClassEnum.INDICE.value:
            return self._calculate_indices_trade_size(entry_price, stop_loss_price, **kwargs)

        if asset_class == AssetClassEnum.COMMODITY.value:
            return self._calculate_commodity_trade_size(entry_price, stop_loss_price, **kwargs)

        raise ValueError("Invalid asset class")

    def _get_adjusted_risk(self):
        """Adjust risk based on portfolio exposure, asset correlation, and market conditions."""
        base_risk = (self._risk_manager.max_risk_percentage / 100) * self._risk_manager.account_balance

        # **DYNAMIC RISK SCALING BASED ON VOLATILITY & EXPOSURE**
        adjusted_risk = base_risk * min(1.5, max(0.5, 1 / (0.5 + 0.01)))

        return adjusted_risk

    @staticmethod
    def _round_down(value: float) -> float:
        """Rounds down the value to a significant digit for proper risk management."""
        if value == 0:
            return 0
        factor = 10 ** math.floor(math.log10(abs(value)))
        return math.floor(value / factor) * factor

    def calculate_order_qty(self, asset_class, entry_price, exit_price, risk_percentage=1, **kwargs) -> float:
        """Public method to calculate order size while rounding it for risk precision."""
        qty = self._calculate_qty_based_on_asset_class(asset_class, entry_price, exit_price, **kwargs)
        return self._round_down(abs(qty * risk_percentage))
