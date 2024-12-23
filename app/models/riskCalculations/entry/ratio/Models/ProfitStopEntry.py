from dataclasses import dataclass


@dataclass
class ProfitStopEntry:
    profit : float
    stop : float
    entry : float
    percentage: float = 0.0  # Default value for percentage

    def setPercentage(self, perc: float):
        self.percentage = perc

