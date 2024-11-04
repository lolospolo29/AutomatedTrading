class RiskManager:
    def __init__(self, maxDrawdown: float, RiskPerTrade: float):
        self.maxDrawdown = maxDrawdown  # Maximaler Verlust in %
        self.riskPerTrade = RiskPerTrade  # Prozentuales Risiko pro Trade
        self.currentDrawdown: float = 0.0  # Aktueller Drawdown

    @staticmethod
    def setNewsTime(time):
        return None

    @staticmethod
    def setcurrentDrawdown(drawdown):
        return None
