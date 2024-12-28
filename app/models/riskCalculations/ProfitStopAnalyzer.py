# Use for Profit as Input
from collections import defaultdict

from app.models.riskCalculations.ProfitStopEntry import ProfitStopEntry
from app.models.riskCalculations.RiskModeEnum import RiskMode


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
    def analyzeByAttribute(entries: list[ProfitStopEntry], x: int, attribute: str) -> list:
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
                ProfitStopAnalyzer.maxProfit,
                ProfitStopAnalyzer.profitAndDistanceTradeoff,
                ProfitStopAnalyzer.optimalProfitEntrySum,
                ProfitStopAnalyzer.optimalProfitStopSum,
            ],
            "stop": [
                ProfitStopAnalyzer.highestStop,
                ProfitStopAnalyzer.lowestStop,
                ProfitStopAnalyzer.maximalDistance,
                ProfitStopAnalyzer.midRangeStop,
            ],
            "entry": [
                ProfitStopAnalyzer.lowestEntry,
                ProfitStopAnalyzer.midRangeEntry,
                ProfitStopAnalyzer.optimalProfitEntrySum,
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
    def analyzeRiskMode(entries: list[ProfitStopEntry], x: int, risk_mode: RiskMode) -> list:
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
                ProfitStopAnalyzer.maxProfit,
                ProfitStopAnalyzer.profitAndDistanceTradeoff,
                ProfitStopAnalyzer.minimalDistance,
            ],
            RiskMode.MODERAT: [
                ProfitStopAnalyzer.midRangeStop,
                ProfitStopAnalyzer.midRangeEntry,
                ProfitStopAnalyzer.optimalProfitEntrySum,
                ProfitStopAnalyzer.optimalProfitStopSum,
            ],
            RiskMode.SAFE: [
                ProfitStopAnalyzer.maximalDistance,
                ProfitStopAnalyzer.highestStop,
                ProfitStopAnalyzer.lowestStop,
                ProfitStopAnalyzer.lowestEntry,
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
    def maxProfit(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit maximalem Profit."""
        return sorted(entries, key=lambda e: e.profit, reverse=True)[:x]

    @staticmethod
    def profitAndDistanceTradeoff(entries: list[ProfitStopEntry], x: int) -> list:
        """Optimierung von Profit mit Bestrafung für große Stop-Entry-Abstände."""
        return sorted(
            entries,
            key=lambda e: e.profit - 2 * abs(e.stop - e.entry),
            reverse=True
        )[:x]

    @staticmethod
    def minimalDistance(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem geringsten Abstand zwischen Stop und Entry."""
        return sorted(entries, key=lambda e: abs(e.stop - e.entry))[:x]

    # Moderat
    @staticmethod
    def midRangeStop(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit mittleren Stop-Werten."""
        return sorted(entries,
                      key=lambda e: abs(e.stop - sum(entry.stop for entry in entries) / len(entries)))[:x]

    @staticmethod
    def midRangeEntry(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit mittleren Entry-Werten."""
        return sorted(entries,
                      key=lambda e: abs(e.entry - sum(entry.entry for entry in entries) / len(entries)))[:x]

    @staticmethod
    def optimalProfitEntrySum(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit der höchsten Summe aus Profit und Entry."""
        return sorted(entries, key=lambda e: e.profit + e.entry, reverse=True)[:x]

    @staticmethod
    def optimalProfitStopSum(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit der höchsten Summe aus Profit und Stop."""
        return sorted(entries, key=lambda e: e.profit + e.stop, reverse=True)[:x]

    # Safe
    @staticmethod
    def maximalDistance(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem größten Abstand zwischen Stop und Entry."""
        return sorted(entries, key=lambda e: abs(e.stop - e.entry), reverse=True)[:x]

    @staticmethod
    def highestStop(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem höchsten Stop-Wert."""
        return sorted(entries, key=lambda e: e.stop, reverse=True)[:x]

    @staticmethod
    def lowestStop(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem niedrigsten Stop-Wert."""
        return sorted(entries, key=lambda e: e.stop)[:x]

    @staticmethod
    def lowestEntry(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem niedrigsten Entry-Wert."""
        return sorted(entries, key=lambda e: e.entry)[:x]

entries = [
    ProfitStopEntry(profit=100, stop=50, entry=10),
    ProfitStopEntry(profit=120, stop=40, entry=15),
    ProfitStopEntry(profit=80, stop=30, entry=5),
    ProfitStopEntry(profit=150, stop=70, entry=20),
]

# Analyze by the 'profit' attribute and get the top 2 entries
top_profit_entries = ProfitStopAnalyzer.analyzeByAttribute(entries, x=2, attribute='profit')
for entry in top_profit_entries:
    print(entry)

# Analyze by the 'entry' attribute and get the top 2 entries
top_entry_entries = ProfitStopAnalyzer.analyzeByAttribute(entries, x=2, attribute='entry')
for entry in top_entry_entries:
    print(entry)

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
# print(ProfitStopAnalyzer.maxProfit(test_entries, x))
#
# print("\nProfit and Distance Tradeoff:")
# print(ProfitStopAnalyzer.profitAndDistanceTradeoff(test_entries, x))
#
# print("\nMinimal Distance:")
# print(ProfitStopAnalyzer.minimalDistance(test_entries, x))
#
# print("\nMid-Range Stop:")
# print(ProfitStopAnalyzer.midRangeStop(test_entries, x))
#
# print("\nMid-Range Entry:")
# print(ProfitStopAnalyzer.midRangeEntry(test_entries, x))
#
# print("\nOptimal Profit Entry Sum:")
# print(ProfitStopAnalyzer.optimalProfitEntrySum(test_entries, x))
#
# print("\nOptimal Profit Stop Sum:")
# print(ProfitStopAnalyzer.optimalProfitStopSum(test_entries, x))
#
# print("\nMaximal Distance:")
# print(ProfitStopAnalyzer.maximalDistance(test_entries, x))
#
# print("\nHighest Stop:")
# print(ProfitStopAnalyzer.highestStop(test_entries, x))
#
# print("\nLowest Stop:")
# print(ProfitStopAnalyzer.lowestStop(test_entries, x))
#
# print("\nLowest Entry:")
# print(ProfitStopAnalyzer.lowestEntry(test_entries, x))