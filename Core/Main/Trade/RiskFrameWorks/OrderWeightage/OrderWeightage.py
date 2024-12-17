

class OrderWeightage:

    def getPercentagePerLevel(self, percentage: float, order_tp_assignments: list[tuple[int, float]],
                              mode: int) -> list[
        tuple[int, float, float]]:
        """
        Verarbeitet die TP-Zuordnungen und verteilt den Prozentsatz basierend auf dem Modus.
        :param mode:
        :param percentage: Gesamtprozentsatz, der auf die Orders verteilt wird.
        :param order_tp_assignments: Liste von Zuordnungen (Order-Index, TP-Level).
        :return: Liste von Zuordnungen (Order-Index, TP-Level, Prozentsatz).
        """
        orderAmount = len(order_tp_assignments)
        if mode == "aggressiv":
            weights = [1 / (i + 1) for i in range(orderAmount)]
        elif mode == "gleichmäßig":
            weights = [1 / orderAmount] * orderAmount
        elif mode == "risikoarm":
            weights = [0.5] + [0.5 / (orderAmount - 1) for _ in range(orderAmount - 1)]
        else:
            raise ValueError("Unbekannter Modus. 'aggressiv', 'gleichmäßig' oder 'risikoarm' erwartet.")

        # Normalisiere die Gewichte
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        # Verteile die Prozentsätze entsprechend der Gewichte
        return [(order, tp, round(percentage * weight, 2)) for (order, tp), weight in
                zip(order_tp_assignments, normalized_weights)]
