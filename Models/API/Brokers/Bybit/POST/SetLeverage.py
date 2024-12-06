from dataclasses import dataclass

from Models.API.POSTParams import POSTParams


# POST /v5/position/set-leverage
@dataclass
class SetLeverage(POSTParams):
    # Required parameter
    category: str
    symbol: str
    buyLeverage: str
    sellLeverage: str

    def validate(self):
        """Validate required parameters."""
        if not self.category and self.symbol and self.buyLeverage and self.sellLeverage:
            raise ValueError("The 'category' parameter is required.")
