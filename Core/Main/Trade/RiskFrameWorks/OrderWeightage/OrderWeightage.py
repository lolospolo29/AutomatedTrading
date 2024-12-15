

class OrderWeightage:

    @staticmethod
    def sortOrderToTPLevel(orderAmount: int, tpLevel: list[float], direction: str,
                           mode: int) -> list[tuple[int, float]]:
        """
        Ordnet die TP-Level den Orders zu, basierend auf dem Modus und der Richtung.
        :param mode:
        :param orderAmount: Anzahl der Orders.
        :param tpLevel: Liste der TP-Level.
        :param direction: Richtung ('long' oder 'short').
        :return: Liste von Zuordnungen (Order-Index, TP-Level).
        """
        if len(tpLevel) < orderAmount:
            raise ValueError("Nicht genügend TP-Level für die Anzahl der Orders.")

        if direction == "Buy":
            tpLevel.sort()  # Aufsteigend für Long
        elif direction == "Sell":
            tpLevel.sort(reverse=True)  # Absteigend für Short
        else:
            raise ValueError("Unbekannte Richtung. 'long' oder 'short' erwartet.")

        if mode == "aggressiv":
            if direction == "Buy":
                assigned_tp = tpLevel[-orderAmount:][::-1]
            elif direction == "Sell":
                assigned_tp = tpLevel[:orderAmount]
        elif mode == "gleichmäßig":
            assigned_tp = tpLevel[:orderAmount]
        elif mode == "risikoarm":
            if direction == "Buy":
                closest_tp = tpLevel[0]
            elif direction == "Sell":
                closest_tp = tpLevel[0]

            tpLevel.remove(closest_tp)
            remaining_tp = tpLevel[:orderAmount - 1]
            assigned_tp = [closest_tp] + remaining_tp
        else:
            raise ValueError("Unbekannter Modus. 'aggressiv', 'gleichmäßig' oder 'risikoarm' erwartet.")

        return [(i + 1, assigned_tp[i]) for i in range(orderAmount)]

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
