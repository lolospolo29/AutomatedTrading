from dataclasses import dataclass


# noinspection PyTypeChecker
@dataclass(frozen=True)
class ProfitStopEntry:
    profit: float
    stop: float
    entry: float
    percentage: float = 0.0  # Default value for percentage

    def setPercentage(self, perc: float):
        object.__setattr__(self, 'percentage', perc)  # Workaround for @dataclass(frozen=True)

    def __hash__(self):
        return hash((self.profit, self.stop, self.entry, self.percentage))

    def __eq__(self, other):
        if not isinstance(other, ProfitStopEntry):
            return NotImplemented
        return (self.profit, self.stop, self.entry, self.percentage) == \
               (other.profit, other.stop, other.entry, other.percentage)

