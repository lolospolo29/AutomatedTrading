
class BreakEven:
    def __init__(self):
        self.percentage = 75

    def IsPriceInBreakEvenRange(self, currentPrice:float, entry: float, takeProfit: float) -> bool:

        # Berechnung des Zielpreises basierend auf der angegebenen Prozentzahl
        targetPrice = entry + (takeProfit - entry) * (self.percentage / 100.0)

        # Prüfen, ob der aktuelle Preis das Ziel erreicht oder überschritten hat
        if entry < takeProfit:
            return currentPrice >= targetPrice
        if entry > takeProfit:
            return currentPrice <= targetPrice
        if entry == takeProfit:
            raise ValueError
