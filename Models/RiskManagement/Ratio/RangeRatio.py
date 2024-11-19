from Interfaces.RiskManagement.IRatio import IRatio


class RangeRatio(IRatio):
    def __init__(self, range: list[int]):
        """
        Initialisiert die RangeRatio-Klasse.
        :param range: Ein Bereich als Liste mit [min, max] Ratio-Werten.
        """
        if len(range) != 2 or range[0] > range[1]:
            raise ValueError("Range muss eine Liste mit zwei Werten [min, max] sein.")
        self.range = range

    def getRatio(self, stop: float, takeProfits: list[float]) -> list[float]:
        """
        Generiert eine Liste von Ratios basierend auf den gegebenen Stop- und Take-Profit-Werten,
        die in der angegebenen Range liegen.
        :param stop: Der Stop-Wert.
        :param takeProfits: Eine Liste von Take-Profit-Werten.
        :return: Eine Liste von Ratios, die in der Range liegen.
        """
        if stop <= 0:
            raise ValueError("Stop muss größer als 0 sein.")
        if not takeProfits:
            raise ValueError("Die Liste der Take-Profits darf nicht leer sein.")

        min_range, max_range = self.range
        ratios = []
        for tp in takeProfits:
            ratio = tp / stop
            if min_range <= ratio <= max_range:
                ratios.append(ratio)
        return ratios
