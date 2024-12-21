# Use for Profit as Input
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Models.ProfitStopEntry import ProfitStopEntry


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
    def closestStopEntry(entries: list[ProfitStopEntry], x: int) -> list:
        """Finde die x Einträge mit dem geringsten Abstand zwischen Stop und Entry."""
        return sorted(entries, key=lambda e: abs(e.stop - e.entry))[:x]

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
