# Use for Profit as Input
from app.models.riskCalculations.entry.ratio.Models.ProfitStopEntry import ProfitStopEntry


class ProfitStopAnalyzer:
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