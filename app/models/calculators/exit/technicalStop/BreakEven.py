from app.monitoring.logging.logging_startup import logger


class BreakEven:
    """Break Even Calculator"""
    def __init__(self):
        self.percentage = 75

    def IsPriceInBreakEvenRange(self, currentPrice:float, entry: float, takeProfit: float) -> bool:
        try:
            # Berechnung des Zielpreises basierend auf der angegebenen Prozentzahl
            targetPrice = entry + (takeProfit - entry) * (self.percentage / 100.0)

            # Prüfen, ob der aktuelle Preis das Ziel erreicht oder überschritten hat
            if entry < takeProfit:
                return currentPrice >= targetPrice
            if entry > takeProfit:
                return currentPrice <= targetPrice
        except Exception as e:
            logger.critical("Exception occurred in BreakEven: {}".format(e))
