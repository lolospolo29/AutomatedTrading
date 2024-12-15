
class RangeRatio:
    def getRatio(self, stop: float, takeProfits: list[float], range: list[int]) -> list[float]:
        """
        Generiert eine Liste von Ratios basierend auf den gegebenen Stop- und Take-Profit-Werten,
        die in der angegebenen Range liegen.
        :param range:
        :param stop: Der Stop-Wert.
        :param takeProfits: Eine Liste von Take-Profit-Werten.
        :return: Eine Liste von Ratios, die in der Range liegen.
        """
        if stop <= 0:
            raise ValueError("Stop muss größer als 0 sein.")
        if not takeProfits:
            raise ValueError("Die Liste der Take-Profits darf nicht leer sein.")

        min_range, max_range = range
        ratios = []
        for tp in takeProfits:
            ratio = tp / stop
            if min_range <= ratio <= max_range:
                ratios.append(ratio)
        return ratios
