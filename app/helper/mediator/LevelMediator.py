from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.level.CBDR import CBDR
from app.models.calculators.frameworks.level.equalHL import equalHL
from app.models.calculators.frameworks.level.fibonnaci.OTE import OTE
from app.models.calculators.frameworks.level.fibonnaci.PD import PD
from app.models.calculators.frameworks.level.fibonnaci.STDV import STDV
from app.models.calculators.frameworks.level.opens.NDOG import NDOG
from app.models.calculators.frameworks.level.opens.NWOG import NWOG
from app.models.calculators.frameworks.level.previous.PreviousDaysLevels import PreviousDaysLevels
from app.models.calculators.frameworks.level.previous.PreviousSessionLevels import PreviousSessionLevels
from app.models.calculators.frameworks.level.previous.PreviousWeekLevels import PreviousWeekLevels
from app.monitoring.logging.logging_startup import logger


# noinspection PyTypeChecker
class LevelMediator:
    """
    Initializes the instance with required submodules and ensures it is only initialized once.

    This constructor instantiates the internal components necessary for the functionality
    of the class. The submodules include `OTE`, `PD`, `STDV`, `CBDR`, and others that are
    related to handling various operational components. To prevent re-initialization, it
    checks for the presence of the `initialized` attribute and skips initialization if it
    is already set.
    """
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LevelMediator, cls).__new__(cls)
        return cls._instance

    # region Initializing
    def __init__(self):

        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self._ote: OTE = OTE()
            self._pd = PD()
            self._stdv = STDV()
            self._cbdr = CBDR()
            self._equal = equalHL()
            self._ndog = NDOG()
            self._nwog = NWOG()
            self._previous_days_level = PreviousDaysLevels()
            self._previous_session_level = PreviousSessionLevels()
            self._previous_week_levels = PreviousWeekLevels()

            self.initialized: bool = True  # Mark as initialized
    # endregion

    # region Calculators / Analyzing
    def calculate_levels(self, level_type: str, candles: list[Candle]) -> list:
        """
        Calculates trading levels based on the specified level type and provided market candle data.

        This method determines trading levels using different strategies depending
        on the provided `level_type`. Each type corresponds to a specific algorithm
        or methodology for calculating levels. The calculation utilizes market data
        encapsulated in the provided `candles` list. The function wraps the logic for
        selecting and invoking the appropriate strategy, ensuring modularity and
        extensibility.

        :param level_type: The type of trading level to calculate. Acceptable values
            include "CBDR", "previousDaysLevels", and "PreviousWeekLevels".
        :param candles: A list of market data, where each element represents a
            market candle and provides information such as open, high, low, and close
            prices.

        :return: A list of calculated trading levels based on the selected
            strategy for the specified type.
        :rtype: list
        """
        try:
            if level_type == "CBDR":
                return self._cbdr.return_levels(candles)
            if level_type == "previousDaysLevels":
                return self._previous_days_level.return_levels(candles)
            if level_type == "PreviousWeekLevels":
                return self._previous_week_levels.return_levels(candles)
        except Exception as e:
            logger.error("Error calculating levels: {}".format(e))

    def calculate_previous_sessions(self, candles: list[Candle], time_windows) -> list:
        """
        Calculates the previous sessions' levels based on provided candle data and time windows. It leverages
        the `_previous_session_level` object's `return_levels` method to compute the levels.
        Handles exceptions by logging an error message.

        :param candles: A list of Candle objects representing the input data for the calculation.
        :type candles: list[Candle]
        :param time_windows: A parameter specifying the time windows to be used for the calculation.
        :return: A list containing the calculated levels for the previous sessions.
        :rtype: list
        """
        try:
            return self._previous_session_level.return_levels(candles, time_windows)
        except Exception as e:
            logger.error("Error calculating previous sessions: {}".format(e))

    def calculate_equal_levels(self, candles: list[Candle], direction: str) -> list:
        """
        Calculates equal levels based on the given series of candles and the direction.

        This method takes a list of candle data and a specified direction to calculate
        equal levels using an internal method `_equal.returnLevels`. It handles any
        exception that may occur during the process and logs the error for debugging
        purposes. The calculated levels are returned as a list.

        :param candles: A list of Candle objects representing market data over a
            period, including details such as open, high, low, and close prices.
        :type candles: list[Candle]
        :param direction: The market direction to use for processing ('up' or 'down').
        :return: A list of calculated levels based on the input candles and direction.
        :rtype: list
        :raises Exception: If an error occurs during the calculation process.
        """
        try:
            return self._equal.returnLevels(candles, direction)
        except Exception as e:
            logger.error("Error calculating equal levels: {}".format(e))

    def calculate_fibonacci(self, level_type, candles: list[Candle], lookback) -> list:
        """
        Calculates Fibonacci levels based on the given level type and a list of candle data. This
        method determines the appropriate level generation process depending on the level type
        provided (e.g., OTE, PD, STDV). It utilizes specialized internal class methods to calculate
        and return the levels.

        :param level_type: A string indicating the type of Fibonacci levels to calculate. The
            available options are "OTE", "PD", or "STDV".
        :param candles: A list containing candle data, where each element is an instance of the
            `Candle` class that holds OHLC data.
        :param lookback: The number of previous candles to consider as part of the lookback
            period when calculating levels.
        :return: A list of calculated Fibonacci levels relevant to the specified type and
            candles provided.
        :rtype: list
        """
        try:
            if level_type == "OTE":
                return self._ote.return_levels(candles, lookback)
            if level_type == "PD":
                return self._pd.return_levels(candles, lookback)
            if level_type == "STDV":
                return self._stdv.return_levels(candles, lookback)
        except Exception as e:
            logger.error("Error calculating levels: {}".format(e))

    def return_opening_gap(self, level_type:str, candles: list[Candle]) -> list:
        """
        Calculates and returns the opening gap levels based on the specified type
        and provided list of candle objects.

        The function determines the type of opening gap level (e.g., NWOG or NDOG)
        and fetches the corresponding levels using internal computation methods.
        If the specified `level_type` is not supported or an error occurs during
        computation, the error is logged.

        :param level_type: Specifies the type of opening gap level to calculate.
        :param candles: List of candle instances used for calculating the
            opening gap levels.
        :return: A list of computed gap levels based on the specified type and
            input candle data.
        :rtype: list
        :raises Exception: Logs any exception that occurs during the calculation.
        """
        try:
            if level_type == "NWOG":
                return self._nwog.return_levels(candles)
            if level_type == "NDOG":
                return self._ndog.return_levels(candles)
        except Exception as e:
            logger.error("Error calculating levels: {}".format(e))
    # endregion



