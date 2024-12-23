from dataclasses import dataclass

from app.API.POSTParams import POSTParams


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
        if self.category and self.symbol and self.buyLeverage and self.sellLeverage:
            return True
        return False
