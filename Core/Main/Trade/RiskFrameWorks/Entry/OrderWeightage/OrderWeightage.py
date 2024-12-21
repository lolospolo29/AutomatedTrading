from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Models.ProfitStopEntry import ProfitStopEntry
from Core.Main.Trade.RiskFrameWorks.RiskModeEnum import RiskMode


class OrderWeightage:

    def setPercentagesBasedOnMode(self, entries:list[ProfitStopEntry], mode: RiskMode) -> list[ProfitStopEntry]:
        total_entries = len(entries)
        if total_entries == 0:
            return entries

        if mode == RiskMode.AGGRESSIVE:
            # Aggressive mode: heavier weight to early entries
            return self._setAggressiveWeightage(entries)
        elif mode == RiskMode.MODERAT:
            # Moderate mode: equal distribution of percentage across entries
            return self._setModerateWeightage(entries)
        elif mode == RiskMode.SAFE:
            # Safe mode: heavier weight to later entries
            return self._setSafeWeightage(entries)

    @staticmethod
    def _setAggressiveWeightage(entries:list[ProfitStopEntry]):
        total_entries = len(entries)
        for i, entry in enumerate(entries):
            # Aggressive: More weight on early entries, less on later ones
            weight = (total_entries - i) / total_entries
            entry.setPercentage(weight * 100)
        return entries

    @staticmethod
    def _setModerateWeightage(entries:list[ProfitStopEntry]):
        # Moderate: Distribute percentages equally
        total_entries = len(entries)
        for entry in entries:
            entry.setPercentage(100 / total_entries)
        return entries

    @staticmethod
    def _setSafeWeightage(entries:list[ProfitStopEntry]):
        total_entries = len(entries)
        for i, entry in enumerate(entries):
            # Safe: More weight on later entries, less on earlier ones
            weight = (i + 1) / total_entries
            entry.setPercentage(weight * 100)
        return entries
