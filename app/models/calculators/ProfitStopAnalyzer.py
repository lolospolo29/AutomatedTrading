# Use for Profit as Input
from collections import defaultdict

from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.RiskModeEnum import RiskMode


class ProfitStopAnalyzer:
    # region Initializing
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProfitStopAnalyzer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self._initialized: bool = True  # Mark as initialized

    @staticmethod
    def analyze_by_attribute(entries: list[ProfitStopEntry], x: int, attribute: str) -> list:
        """
        Analyzes entries based on the specified attribute ('profit', 'stop', or 'entry')
        and sorts them by aggregating their ranks across relevant methods.

        Args:
            entries (list[ProfitStopEntry]): List of ProfitStopEntry instances.
            x (int): Number of entries to return.
            attribute (str): Attribute to analyze ('profit', 'stop', 'entry').

        Returns:
            list[ProfitStopEntry]: Sorted list of entries based on aggregated ranks.
        """
        attribute_methods = {
            "profit": [
                ProfitStopAnalyzer.max_profit,
                ProfitStopAnalyzer.profit_and_distance_tradeoff,
                ProfitStopAnalyzer.optimal_profit_entry_sum,
                ProfitStopAnalyzer.optimal_profit_stop_sum,
            ],
            "stop": [
                ProfitStopAnalyzer.highest_stop,
                ProfitStopAnalyzer.lowest_stop,
                ProfitStopAnalyzer.maximal_distance,
                ProfitStopAnalyzer.mid_range_stop,
            ],
            "entry": [
                ProfitStopAnalyzer.lowest_entry,
                ProfitStopAnalyzer.mid_range_entry,
                ProfitStopAnalyzer.optimal_profit_entry_sum,
            ],
        }

        if attribute not in attribute_methods:
            raise ValueError(f"Invalid attribute: {attribute}. Choose from {list(attribute_methods.keys())}.")

        # Get relevant methods for the specified attribute
        methods = attribute_methods[attribute]

        # Aggregate rankings from all relevant methods
        rankings = defaultdict(int)  # To store cumulative rankings for each entry
        for method in methods:
            ranked_list = method(entries, len(entries))  # Get the full ranked list from each method
            for rank, entry in enumerate(ranked_list):
                rankings[entry] += rank  # Add the rank from this method

        # Sort entries by cumulative ranking score
        sorted_entries = sorted(entries, key=lambda e: rankings[e])

        # Return the top `x` entries
        return sorted_entries[:x]

    @staticmethod
    def analyze_risk_mode(entries: list[ProfitStopEntry], x: int, risk_mode: RiskMode) -> list:
        """
        Analyzes entries based on the specified risk mode ('aggressiv', 'moderat', 'safe') and sorts
        them by aggregating their ranks across the relevant methods for that risk mode.

        Args:
            entries (list[ProfitStopEntry]): List of ProfitStopEntry instances.
            x (int): Number of entries to return.
            risk_mode (str): Risk mode ('aggressiv', 'moderat', 'safe').

        Returns:
            list[ProfitStopEntry]: Sorted list of entries based on aggregated ranks.
        """
        risk_mode_methods = {
            RiskMode.AGGRESSIVE: [
                ProfitStopAnalyzer.max_profit,
                ProfitStopAnalyzer.profit_and_distance_tradeoff,
                ProfitStopAnalyzer.minimal_distance,
            ],
            RiskMode.MODERAT: [
                ProfitStopAnalyzer.mid_range_stop,
                ProfitStopAnalyzer.mid_range_entry,
                ProfitStopAnalyzer.optimal_profit_entry_sum,
                ProfitStopAnalyzer.optimal_profit_stop_sum,
            ],
            RiskMode.SAFE: [
                ProfitStopAnalyzer.maximal_distance,
                ProfitStopAnalyzer.highest_stop,
                ProfitStopAnalyzer.lowest_stop,
                ProfitStopAnalyzer.lowest_entry,
            ],
        }

        if risk_mode not in risk_mode_methods:
            raise ValueError(f"Invalid risk mode: {risk_mode}. Choose from {list(risk_mode_methods.keys())}.")

        # Get relevant methods for the specified risk mode
        methods = risk_mode_methods[risk_mode]

        # Aggregate rankings from all relevant methods
        rankings = defaultdict(int)  # To store cumulative rankings for each entry
        for method in methods:
            ranked_list = method(entries, len(entries))  # Get the full ranked list from each method
            for rank, entry in enumerate(ranked_list):
                rankings[entry] += rank  # Add the rank from this method

        # Sort entries by cumulative ranking score
        sorted_entries = sorted(entries, key=lambda e: rankings[e])

        # Return the top `x` entries
        return sorted_entries[:x]

    # Aggressiv
    @staticmethod
    def max_profit(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit maximalem Profit."""
        return sorted(entries, key=lambda e: e.profit, reverse=True)[:x]

    @staticmethod
    def profit_and_distance_tradeoff(entries: list[ProfitStopEntry], x: int) -> list:
        """Optimierung von Profit mit Bestrafung für große Stop-Entry-Abstände."""
        return sorted(
            entries,
            key=lambda e: e.profit - 2 * abs(e.stop - e.entry),
            reverse=True
        )[:x]

    @staticmethod
    def minimal_distance(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem geringsten Abstand zwischen Stop und Entry."""
        return sorted(entries, key=lambda e: abs(e.stop - e.entry))[:x]

    # Moderat
    @staticmethod
    def mid_range_stop(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit mittleren Stop-Werten."""
        return sorted(entries,
                      key=lambda e: abs(e.stop - sum(entry.stop for entry in entries) / len(entries)))[:x]

    @staticmethod
    def mid_range_entry(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit mittleren Entry-Werten."""
        return sorted(entries,
                      key=lambda e: abs(e.entry - sum(entry.entry for entry in entries) / len(entries)))[:x]

    @staticmethod
    def optimal_profit_entry_sum(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit der höchsten Summe aus Profit und Entry."""
        return sorted(entries, key=lambda e: e.profit + e.entry, reverse=True)[:x]

    @staticmethod
    def optimal_profit_stop_sum(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit der höchsten Summe aus Profit und Stop."""
        return sorted(entries, key=lambda e: e.profit + e.stop, reverse=True)[:x]

    # Safe
    @staticmethod
    def maximal_distance(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem größten Abstand zwischen Stop und Entry."""
        return sorted(entries, key=lambda e: abs(e.stop - e.entry), reverse=True)[:x]

    @staticmethod
    def highest_stop(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem höchsten Stop-Wert."""
        return sorted(entries, key=lambda e: e.stop, reverse=True)[:x]

    @staticmethod
    def lowest_stop(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem niedrigsten Stop-Wert."""
        return sorted(entries, key=lambda e: e.stop)[:x]

    @staticmethod
    def lowest_entry(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem niedrigsten Entry-Wert."""
        return sorted(entries, key=lambda e: e.entry)[:x]

# entries = [
#     ProfitStopEntry(profit=100, stop=25, entry=50),
#     ProfitStopEntry(profit=120, stop=40, entry=60),
#     ProfitStopEntry(profit=80, stop=30, entry=40),
#     ProfitStopEntry(profit=150, stop=50, entry=60),
#     ProfitStopEntry(profit=200, stop=50, entry=60),
#     ProfitStopEntry(profit=300, stop=50, entry=60),
#     ProfitStopEntry(profit=400, stop=50, entry=60),
# ]
#
# # Analyze by the 'profit' attribute and get the top 2 entries
# profitentries = ProfitStopAnalyzer.analyze_by_attribute(entries, x=4, attribute='profit')
# for entry in profitentries:
#     print(entry)
# print()
#
# # Analyze by the 'entry' attribute and get the top 2 entries
# entryentries = ProfitStopAnalyzer.analyze_by_attribute(entries, x=4, attribute='entry')
# for entry in entryentries:
#     print(entry)
#
# print()
#
# stopentries = ProfitStopAnalyzer.analyze_by_attribute(entries, x=4, attribute='stop')
# for entry in stopentries:
#     print(entry)
#
# print()
#
# riskmodesafe = ProfitStopAnalyzer.analyze_risk_mode(entries, x=2, risk_mode=RiskMode.SAFE)
# for entry in riskmodesafe:
#     print(entry)
#
# print()
# riskmodemoderat = ProfitStopAnalyzer.analyze_risk_mode(entries, x=2, risk_mode=RiskMode.MODERAT)
# for entry in riskmodemoderat:
#     print(entry)
#
# print()
#
# riskmodeaggressive = ProfitStopAnalyzer.analyze_risk_mode(entries, x=2, risk_mode=RiskMode.AGGRESSIVE)
# for entry in riskmodeaggressive:
#     print(entry)

# Generate a list of test entries
#
# # Test entries
# test_entries = [ProfitStopEntry(120,150,130),ProfitStopEntry(110,160,120),ProfitStopEntry(100,130,120)
#     ,ProfitStopEntry(99,120,100),ProfitStopEntry(130,150,140)]
# # Testing each function
# x = 5  # Number of entries to retrieve
# print("Original Entries:")
# for entry in test_entries:
#     print(entry)
#
# print("\nMax Profit:")
# print(ProfitStopAnalyzer.max_profit(test_entries, x))
#
# print("\nProfit and Distance Tradeoff:")
# print(ProfitStopAnalyzer.profit_and_distance_tradeoff(test_entries, x))
#
# print("\nMinimal Distance:")
# print(ProfitStopAnalyzer.minimal_distance(test_entries, x))
#
# print("\nMid-Range Stop:")
# print(ProfitStopAnalyzer.mid_range_stop(test_entries, x))
#
# print("\nMid-Range Entry:")
# print(ProfitStopAnalyzer.mid_range_entry(test_entries, x))
#
# print("\nOptimal Profit Entry Sum:")
# print(ProfitStopAnalyzer.optimal_profit_entry_sum(test_entries, x))
#
# print("\nOptimal Profit Stop Sum:")
# print(ProfitStopAnalyzer.optimal_profit_stop_sum(test_entries, x))
#
# print("\nMaximal Distance:")
# print(ProfitStopAnalyzer.maximal_distance(test_entries, x))
#
# print("\nHighest Stop:")
# print(ProfitStopAnalyzer.highest_stop(test_entries, x))
#
# print("\nLowest Stop:")
# print(ProfitStopAnalyzer.lowest_stop(test_entries, x))
#
# print("\nLowest Entry:")
# print(ProfitStopAnalyzer.lowest_entry(test_entries, x))