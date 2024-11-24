from Interfaces.RiskManagement.IRatio import IRatio


class FixedRatio(IRatio):
    def getRatio(self, stop: float, ratio: int) -> float:
        """
        Berechnet die Zielgröße basierend auf dem Stop und der Ratio.
        :param ratio:
        :param stop: Der gegebene Stop-Wert.
        :return: Das berechnete Ziel.
        """
        if stop <= 0:
            raise ValueError("Stop muss größer als 0 sein.")
        return stop * ratio

