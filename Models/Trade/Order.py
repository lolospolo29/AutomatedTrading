class Order:
    def __init__(self):
        self.status: str = ""
        self.id: int = 0
        self.stopLoss: float = 0.0
        self.takeProfit: float = 0.0
        self.riskPercentage: float = 0.0

    def toDict(self):
        """Gibt alle Datenpunkte als Dictionary zurück, inklusive timeStamp."""
        # Zeitformatierung: Entfernt Datum und gibt nur die Uhrzeit zurück

        return {
            "status": self.status,
            "id": self.id,
            "stopLoss": self.stopLoss,
            "takeProfit": self.takeProfit,
            "riskPercentage": self.riskPercentage,
        }
