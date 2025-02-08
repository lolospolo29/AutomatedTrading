# Use for Profit as Input
from collections import defaultdict

from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.RiskModeEnum import RiskMode
from app.monitoring.logging.logging_startup import logger


# noinspection PyTypeChecker
class ProfitStopEntrySorter:
    # region Initializing
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProfitStopEntrySorter, cls).__new__(cls)
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
        logger.Info("Analyzing ProfitStop Entry By Attribute:{count}".format(count=len(entries)))

        try:
            attribute_methods = {
                "profit": [
                    ProfitStopEntrySorter.max_profit,
                    ProfitStopEntrySorter.profit_and_distance_tradeoff,
                    ProfitStopEntrySorter.optimal_profit_entry_sum,
                    ProfitStopEntrySorter.optimal_profit_stop_sum,
                ],
                "stop": [
                    ProfitStopEntrySorter.highest_stop,
                    ProfitStopEntrySorter.lowest_stop,
                    ProfitStopEntrySorter.maximal_distance,
                    ProfitStopEntrySorter.mid_range_stop,
                ],
                "entry": [
                    ProfitStopEntrySorter.lowest_entry,
                    ProfitStopEntrySorter.mid_range_entry,
                    ProfitStopEntrySorter.optimal_profit_entry_sum,
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
        except Exception as ex:
            logger.critical(f"An error occurred in Profit Stop Analyzer: {ex}")

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
        logger.Info("Analyzing ProfitStop Entry By Risk Mode:{count}".format(count=len(entries)))

        try:
            risk_mode_methods = {
                RiskMode.AGGRESSIVE: [
                    ProfitStopEntrySorter.max_profit,
                    ProfitStopEntrySorter.profit_and_distance_tradeoff,
                    ProfitStopEntrySorter.minimal_distance,
                ],
                RiskMode.MODERAT: [
                    ProfitStopEntrySorter.mid_range_stop,
                    ProfitStopEntrySorter.mid_range_entry,
                    ProfitStopEntrySorter.optimal_profit_entry_sum,
                    ProfitStopEntrySorter.optimal_profit_stop_sum,
                ],
                RiskMode.SAFE: [
                    ProfitStopEntrySorter.maximal_distance,
                    ProfitStopEntrySorter.highest_stop,
                    ProfitStopEntrySorter.lowest_stop,
                    ProfitStopEntrySorter.lowest_entry,
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
        except Exception as e:
            logger.critical(f"An error occurred in Profit Stop Analyzer: {e}")

    # Aggressiv
    @staticmethod
    def max_profit(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Calculate the maximum profit entries from the given list of ProfitStopEntry objects.

        The function sorts the entries based on their profit value in descending order
        and returns the top `x` entries from the sorted list.

        :param entries: A list of ProfitStopEntry objects to be evaluated.
        :type entries: list[ProfitStopEntry]
        :param x: The number of top entries to be returned from the sorted list.
        :type x: int
        :return: A list of the top `x` ProfitStopEntry objects based on their profit values.
        :rtype: list
        """
        return sorted(entries, key=lambda e: e.profit, reverse=True)[:x]

    @staticmethod
    def profit_and_distance_tradeoff(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Sorts a list of profit stop entries based on a trade-off between profit and
        distance, returning the top x entries. The trade-off is calculated by
        subtracting twice the absolute difference between the stop and entry values
        from the profit. The higher this resulting value, the higher priority the
        entry receives in the sorted list. The returned list is sorted in descending
        order of priority.

        :param entries:
            A list of ProfitStopEntry objects to be sorted based on profit and a
            distance tradeoff.
        :param x:
            An integer indicating the number of top entries to return.
        :return:
            A list containing the top x ProfitStopEntry objects based on
            trade-off calculation.
        """
        return sorted(
            entries,
            key=lambda e: e.profit - 2 * abs(e.stop - e.entry),
            reverse=True
        )[:x]

    @staticmethod
    def minimal_distance(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Calculates and returns the subset of entries with the minimal distance
        between their `stop` and `entry` values. This is determined by sorting
        the input entries by the absolute difference (`|stop - entry|`) in ascending
        order and selecting the top `x` entries with the smallest distances.

        :param entries: A list of ProfitStopEntry objects containing `stop` and
            `entry` attributes used for distance calculation.
        :param x: The number of entries to return after sorting by minimal distance.
        :return: A list of the top `x` ProfitStopEntry objects based on minimal
            distance between their `stop` and `entry` values.
        """
        return sorted(entries, key=lambda e: abs(e.stop - e.entry))[:x]

    # Moderat
    @staticmethod
    def mid_range_stop(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Calculate and return the list of entries closest to the median stop value.

        This method finds entries whose stop values are closest to the median stop
        value based on the absolute difference. It then returns the top `x` entries
        sorted by their proximity to this median value.

        :param entries: A list of ProfitStopEntry objects, each containing attributes
            relevant for determining proximity to the median stop.
        :param x: An integer value specifying the number of closest entries to retrieve.
        :return: A list of `ProfitStopEntry` objects sorted by their absolute difference
            from the median stop value.
        """
        return sorted(entries,
                      key=lambda e: abs(e.stop - sum(entry.stop for entry in entries) / len(entries)))[:x]

    @staticmethod
    def mid_range_entry(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Calculates and returns a list of entries with values that are closer to the
        mid-range of the provided entries. The mid-range is computed based on the
        average of the ``entry`` attribute of the given ``entries``. Only the top ``x``
        entries closest to the mid-range are selected. The entries are sorted in
        ascending order of their distance from the mid-range, and the resulting list
        contains up to ``x`` entries.

        :param entries: A list of ``ProfitStopEntry`` objects, where each object
            contains an ``entry`` attribute used for computation.
        :type entries: list[ProfitStopEntry]
        :param x: The maximum number of entries to return, which are closest to the
            computed mid-range value.
        :type x: int
        :return: A list of up to ``x`` ``ProfitStopEntry`` objects, sorted by their
            proximity to the mid-range of all entries.
        :rtype: list[ProfitStopEntry]
        """
        return sorted(entries,
                      key=lambda e: abs(e.entry - sum(entry.entry for entry in entries) / len(entries)))[:x]

    @staticmethod
    def optimal_profit_entry_sum(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Sorts a list of profit stop entries by the sum of their profit and entry values in descending
        order and returns the top X entries according to this criterion.

        :param entries: A list of ProfitStopEntry objects to be evaluated.
        :param x: The number of top entries to return.
        :return: A list containing the top X ProfitStopEntry objects sorted by their profit and entry
                 sum in descending order.
        """
        return sorted(entries, key=lambda e: e.profit + e.entry, reverse=True)[:x]

    @staticmethod
    def optimal_profit_stop_sum(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Determines the `x` entries with the highest combined `profit` and `stop` values
        from a list of `ProfitStopEntry` objects. The method sorts the entries in
        descending order based on the sum of their `profit` and `stop` attributes
        and returns the top `x` entries.

        :param entries:
            A list of `ProfitStopEntry` objects representing the entries to be sorted.
        :param x:
            An integer specifying the number of top entries to return based on the
            combined `profit` and `stop` values.
        :return:
            A list of `ProfitStopEntry` objects representing the top `x` entries
            sorted by the combined value of their `profit` and `stop` attributes.
        """
        return sorted(entries, key=lambda e: e.profit + e.stop, reverse=True)[:x]

    # Safe
    @staticmethod
    def maximal_distance(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Calculate the maximum distance between stop and entry prices for a given number
        of profit stop entries.

        This method sorts the entries based on the absolute difference between the
        `stop` and `entry` attributes in descending order, and limits the output to the
        top `x` entries with the greatest distance.

        :param entries: A list of ProfitStopEntry objects, where each entry contains
            `stop` and `entry` attributes.
        :param x: The number of top entries to be included in the resulting list,
            sorted by maximal distance.
        :return: A list of the top `x` ProfitStopEntry objects sorted by their maximum
            absolute distance between stop and entry.
        """
        return sorted(entries, key=lambda e: abs(e.stop - e.entry), reverse=True)[:x]

    @staticmethod
    def highest_stop(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Determines the highest 'x' entries from the provided list based on the 'stop' attribute.

        This static method sorts the given list of `ProfitStopEntry` objects in descending
        order based on their `stop` attribute. It then retrieves the top 'x' entries
        from the sorted list.

        :param entries: A list of `ProfitStopEntry` objects, where each object contains
            a 'stop' attribute that signifies a stopping value.
        :param x: An integer indicating the number of top entries to return after sorting.
        :return: A new list of `ProfitStopEntry` objects representing the 'x' highest
            stop values available.
        """
        return sorted(entries, key=lambda e: e.stop, reverse=True)[:x]

    @staticmethod
    def lowest_stop(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Determine the lowest 'stop' values from a list of ProfitStopEntry objects.

        This method sorts the provided list of ProfitStopEntry objects by their
        'stop' attribute in ascending order and then returns the specified
        number of entries with the smallest 'stop' values.

        :param entries: A list of ProfitStopEntry objects to be sorted and filtered.
        :type entries: list[ProfitStopEntry]

        :param x: The number of lowest stop values to return after sorting.
        :type x: int

        :return: A list containing the 'x' ProfitStopEntry objects with the lowest
            'stop' values.
        :rtype: list[ProfitStopEntry]
        """
        return sorted(entries, key=lambda e: e.stop)[:x]

    @staticmethod
    def lowest_entry(entries: list[ProfitStopEntry], x: int) -> list:
        """
        Finds the lowest `x` entries from the given list of ProfitStopEntry `entries`.
        The entries are sorted by the `entry` attribute in ascending order, and then the
        first `x` entries are selected and returned.

        :param entries: A list of ProfitStopEntry objects to be sorted and filtered.
        :type entries: list[ProfitStopEntry]
        :param x: The number of lowest entries to retrieve from the list.
        :type x: int
        :return: A list containing the lowest `x` entries from `entries`, sorted by
            the `entry` attribute.
        :rtype: list[ProfitStopEntry]
        """
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