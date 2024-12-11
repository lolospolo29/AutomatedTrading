from Core.Main.Trade import Order


class Trade:

    def __init__(self, asset: str, strategy: str, broker: str):
        self.status: str = "Inactive"
        self.asset: str = asset
        self.strategy = strategy
        self.broker: str = broker
        self.orders: list[Order] = []
        self.pnl: float = 0

    def toDict(self):
        """Gibt alle Datenpunkte als Dictionary zurück, inklusive timeStamp."""
        # Zeitformatierung: Entfernt Datum und gibt nur die Uhrzeit zurück

        return {
            "Trade": {
                "status": self.status,
                "asset": self.asset,
                "orders": [order.toDict() for order in self.orders],  # Convert each order to a dict
                "strategyName": self.strategyName,
                "pnl": self.pnl,
            }
        }
