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


class LevelMediator:
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
        return self._previous_session_level.return_levels(candles, time_windows)

    def calculate_equal_levels(self, candles: list[Candle], direction: str) -> list:
        return self._equal.returnLevels(candles, direction)

    def calculate_fibonacci(self, level_type, candles: list[Candle], lookback) -> list:
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
        try:
            if level_type == "NWOG":
                return self._nwog.return_levels(candles)
            if level_type == "NDOG":
                return self._ndog.return_levels(candles)
        except Exception as e:
            logger.error("Error calculating levels: {}".format(e))
    # endregion



