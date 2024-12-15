from dataclasses import dataclass


@dataclass
class ProfitStopEntry:
    profit : float
    stop : float
    entry : float
