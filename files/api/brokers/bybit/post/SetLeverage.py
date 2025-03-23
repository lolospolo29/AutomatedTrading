from pydantic import BaseModel

# post /v5/position/set-leverage
class SetLeverage(BaseModel):
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
