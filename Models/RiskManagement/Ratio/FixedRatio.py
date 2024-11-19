from Interfaces.RiskManagement.IRatio import IRatio


class FixedRatio(IRatio):
    def __init__(self, ratio):
        self.ratio = ratio

    def getRatio(self, stop: float) -> float:
        """
        Berechnet die Zielgröße basierend auf dem Stop und der Ratio.
        :param stop: Der gegebene Stop-Wert.
        :return: Das berechnete Ziel.
        """
        if stop <= 0:
            raise ValueError("Stop muss größer als 0 sein.")
        return stop * self.ratio

