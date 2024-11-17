from Interfaces.RiskManagement.IOrderWeightage import IOrderWeightage


class OrderWeightage(IOrderWeightage):
    def __init__(self, mode: str):
        """
        Initialisiert das OrderWeightage-Objekt mit einem bestimmten Modus.
        :param mode: Modus der Gewichtung ('aggressiv', 'gleichmäßig', 'risikoarm').
        """
        self.mode = mode

    def sortOrderToTPLevel(self, orderAmount: int, tpLevel: list[float], direction: str) -> list[tuple[int, float]]:
        """
        Ordnet die TP-Level den Orders zu, basierend auf dem Modus und der Richtung.
        :param orderAmount: Anzahl der Orders.
        :param tpLevel: Liste der TP-Level.
        :param direction: Richtung ('long' oder 'short').
        :return: Liste von Zuordnungen (Order-Index, TP-Level).
        """
        if len(tpLevel) < orderAmount:
            raise ValueError("Nicht genügend TP-Level für die Anzahl der Orders.")

        if direction == "long":
            tpLevel.sort()  # Aufsteigend für Long
        elif direction == "short":
            tpLevel.sort(reverse=True)  # Absteigend für Short
        else:
            raise ValueError("Unbekannte Richtung. 'long' oder 'short' erwartet.")

        if self.mode == "aggressiv":
            if direction == "long":
                assigned_tp = tpLevel[-orderAmount:][::-1]
            elif direction == "short":
                assigned_tp = tpLevel[:orderAmount]
        elif self.mode == "gleichmäßig":
            assigned_tp = tpLevel[:orderAmount]
        elif self.mode == "risikoarm":
            if direction == "long":
                closest_tp = tpLevel[0]
            elif direction == "short":
                closest_tp = tpLevel[0]

            tpLevel.remove(closest_tp)
            remaining_tp = tpLevel[:orderAmount - 1]
            assigned_tp = [closest_tp] + remaining_tp
        else:
            raise ValueError("Unbekannter Modus. 'aggressiv', 'gleichmäßig' oder 'risikoarm' erwartet.")

        return [(i + 1, assigned_tp[i]) for i in range(orderAmount)]

    def getPercentagePerLevel(self, percentage: float, order_tp_assignments: list[tuple[int, float]]) -> list[
        tuple[int, float, float]]:
        """
        Verarbeitet die TP-Zuordnungen und verteilt den Prozentsatz basierend auf dem Modus.
        :param percentage: Gesamtprozentsatz, der auf die Orders verteilt wird.
        :param order_tp_assignments: Liste von Zuordnungen (Order-Index, TP-Level).
        :return: Liste von Zuordnungen (Order-Index, TP-Level, Prozentsatz).
        """
        orderAmount = len(order_tp_assignments)
        if self.mode == "aggressiv":
            weights = [1 / (i + 1) for i in range(orderAmount)]
        elif self.mode == "gleichmäßig":
            weights = [1 / orderAmount] * orderAmount
        elif self.mode == "risikoarm":
            weights = [0.5] + [0.5 / (orderAmount - 1) for _ in range(orderAmount - 1)]
        else:
            raise ValueError("Unbekannter Modus. 'aggressiv', 'gleichmäßig' oder 'risikoarm' erwartet.")

        # Normalisiere die Gewichte
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        # Verteile die Prozentsätze entsprechend der Gewichte
        return [(order, tp, round(percentage * weight, 2)) for (order, tp), weight in
                zip(order_tp_assignments, normalized_weights)]
