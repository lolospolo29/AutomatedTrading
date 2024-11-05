class RiskManager:
    def __init__(self, maxDrawdown: float, riskPerTrade: float):
        self.maxDrawdown: float = maxDrawdown  # Maximaler Verlust in %
        self.riskPerTrade: float = riskPerTrade  # Prozentuales Risiko pro Trade
        self.currentDrawdown: float = 0.0  # Aktueller Drawdown

    @staticmethod
    def setNewsTime(time):
        return None

    @staticmethod
    def setcurrentDrawdown(drawdown):
        return None
