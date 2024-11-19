from Interfaces.RiskManagement.ITechnicalStop import ITechnicalStop


class BreakEven(ITechnicalStop):
    def __init__(self, percentage):
        self.percentage = percentage

    def moveExit(self,currentPrice:float,entry: float,takeProfit: float) -> bool:
        if entry == takeProfit:
            raise ValueError("Entry und Take-Profit dürfen nicht gleich sein.")

        # Berechnung des Zielpreises basierend auf der angegebenen Prozentzahl
        targetPrice = entry + (takeProfit - entry) * (self.percentage / 100.0)

        # Prüfen, ob der aktuelle Preis das Ziel erreicht oder überschritten hat
        return currentPrice >= targetPrice

