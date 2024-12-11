from Interfaces.RiskManagement.IMartingale import IMartingale


class AntiMartingale(IMartingale):
    def getOrderAmount(self, ratio: int ,mode :int):
        """
        Berechnet die Anzahl der Orders basierend auf dem Modus und dem Verhältnis.

        :param mode:
        :param ratio: Das Verhältnis, das auf die Orders aufgeteilt wird.
        :return: Die Anzahl der Orders.
        """
        if mode == 1:  # Aggressiv
            return max(1, ratio // 3)  # Eine Order oder weniger Orders (je nach Logik)
        elif mode == 2:  # Moderat
            return max(1, ratio // 2)  # Mittlere Anzahl an Orders
        elif mode == 3:  # Risikoarm
            return ratio  # Mehr Orders, verteilt auf das Verhältnis

    def getMartingaleModel(self, pnl: float):
        if pnl > 0:
            return True
        return False
