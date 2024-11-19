from Interfaces.RiskManagement.IMartingale import IMartingale


class Martingale(IMartingale):
    def __init__(self, mode):
        """
        Initialisiert den AntiMartingale mit einem bestimmten Modus.

        :param mode: 1 = aggressiv, 2 = moderat, 3 = risikoarm
        """
        self.mode: int = mode

    def getOrderAmount(self, ratio: int):
        """
        Berechnet die Anzahl der Orders basierend auf dem Modus und dem Verhältnis.

        :param ratio: Das Verhältnis, das auf die Orders aufgeteilt wird.
        :return: Die Anzahl der Orders.
        """
        if self.mode == 1:  # Aggressiv
            return max(1, ratio // 3)  # Eine Order oder weniger Orders (je nach Logik)
        elif self.mode == 2:  # Moderat
            return max(1, ratio // 2)  # Mittlere Anzahl an Orders
        elif self.mode == 3:  # Risikoarm
            return ratio  # Mehr Orders, verteilt auf das Verhältnis

    def getMartingaleModel(self, currentDrawDown: float):
        if currentDrawDown < 0:
            return True
        return False
