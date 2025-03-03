from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.RiskModeEnum import RiskMode
from app.monitoring.logging.logging_startup import logger


class OrderWeightage:

    def set_percentages_based_on_mode(self, entries:list[ProfitStopEntry], mode: RiskMode) -> list[ProfitStopEntry]:
        """
        Set the Risk Percentages on the Entries with Weightage .

        Returns:
            ProfitStopEntry (list[ProfitStopEntry]) with Percentages based on the mode.
        """
        try:
            logger.info("Set Percentages Based on Mode:{mode},length:{coutn}".format(mode=mode,coutn=len(entries)))
            total_entries = len(entries)
            if total_entries == 0:
                return entries

            if mode == RiskMode.AGGRESSIVE:
                # Aggressive mode: heavier weight to early entries
                return self._set_aggressive_weightage(entries)
            elif mode == RiskMode.MODERAT:
                # Moderate mode: equal distribution of percentage across entries
                return self._set_moderate_weightage(entries)
            elif mode == RiskMode.SAFE:
                # Safe mode: heavier weight to later entries
                return self._set_safe_weightage(entries)
        except Exception as e:
            logger.error("Order Weightage Exception: {}".format(e))


    @staticmethod
    def _set_aggressive_weightage(entries:list[ProfitStopEntry]):
        total_entries = len(entries)
        for i, entry in enumerate(entries):
            # Aggressive: More weight on early entries, less on later ones
            weight = (total_entries - i) / total_entries
            entry.setPercentage(weight * 100)
        return entries

    @staticmethod
    def _set_moderate_weightage(entries:list[ProfitStopEntry]):
        # Moderate: Distribute percentages equally
        total_entries = len(entries)
        for entry in entries:
            entry.setPercentage(100 / total_entries)
        return entries

    @staticmethod
    def _set_safe_weightage(entries:list[ProfitStopEntry]):
        total_entries = len(entries)
        for i, entry in enumerate(entries):
            # Safe: More weight on later entries, less on earlier ones
            weight = (i + 1) / total_entries
            entry.setPercentage(weight * 100)
        return entries
