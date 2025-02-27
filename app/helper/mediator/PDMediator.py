from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.helper.calculator.framework.pdarray.BPR import BPR
from app.helper.calculator.framework.pdarray.Breaker import Breaker
from app.helper.calculator.framework.pdarray.FVG import FVG
from app.helper.calculator.framework.pdarray.OrderBlock import Orderblock
from app.helper.calculator.framework.pdarray.RejectionBlock import RejectionBlock
from app.helper.calculator.framework.pdarray.Swings import Swings
from app.helper.calculator.framework.pdarray.Void import Void
from app.helper.calculator.framework.pdarray.VolumeImbalance import VolumeImbalance
from app.monitoring.logging.logging_startup import logger


# noinspection PyTypeChecker
class PDMediator:
    """
    Handles price discovery computations using multiple analytical approaches,
    designed as a singleton with methods to calculate, analyze, and retrieve
    price-related data.

    The class provides methods to perform computations across various
    price discovery methods such as BPR, FVG, Order Blocks, and more.
    It ensures efficient reusability and centralized data handling by
    using a singleton pattern. By invoking different helper objects,
    it simplifies the implementation and integrates multiple strategies
    for price discovery-related analytics.

    :ivar _bpr: Instance handling BPR (Balanced Price Range) computations.
    :type _bpr: BPR
    :ivar _fvg: Instance handling FVG (Fair Value Gap) computations.
    :type _fvg: FVG
    :ivar _breaker: Instance managing Breaker computations with
                    defined thresholds.
    :type _breaker: Breaker
    :ivar _orderBlock: Instance managing Order Block computations.
    :type _orderBlock: Orderblock
    :ivar _rejection_block: Instance executing Rejection Block computations
                            with predefined parameters.
    :type _rejection_block: RejectionBlock
    :ivar _swings: Instance managing Swings-related computations for
                   price analysis.
    :type _swings: Swings
    :ivar _void: Instance handling computations based on the Void concept.
    :type _void: Void
    :ivar _volume_imbalance: Instance managing Volume Imbalance calculations
                            and analytics.
    :type _volume_imbalance: VolumeImbalance
    :ivar initialized: Boolean flag indicating whether the instance
                       has been initialized to prevent redundant setup.
    :type initialized: bool
    """
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PDMediator, cls).__new__(cls)
        return cls._instance

    # region Initializing
    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self._bpr: BPR = BPR()
            self._fvg = FVG()
            self._breaker: Breaker = Breaker(5)
            self._orderBlock: Orderblock = Orderblock()
            self._rejection_block: RejectionBlock = RejectionBlock(10)
            self._swings: Swings = Swings()
            self._void: Void = Void()
            self._volume_imbalance: VolumeImbalance = VolumeImbalance()
            self.initialized: bool = True  # Mark as initialized
    # endregion

    # region Calculating / Analyzing
    def calculate_pd_array_with_lookback(self, pd_type: str, candles: list[Candle], lookback) -> list:
        """
        Calculates an array of price discovery (PD) values based on the specified type
        and a list of candlestick data. The calculation varies depending on the PD type
        provided. This method integrates various PD computation strategies, such as
        FVG, OB, Swings, Void, and Volume Imbalance, using helper methods or classes.
        If an unsupported PD type is provided, the behavior is unspecified.

        :param pd_type: Defines the type of price discovery to calculate.
        :param candles: A list of `Candle` objects containing the candlestick data
            used in the calculations.
        :param lookback: An int value or similar specifying the number of previously
            nested data points to include in the calculation.
        :return: A list containing the calculated array of PD values based on the
            provided type and input candlestick data.
        :raises Exception: If an error occurs during the computation of PD values,
            it logs the error and raises an Exception.
        """
        try:
            if pd_type == "FVG":
                    return self._fvg.return_array_list(candles, lookback)
            if pd_type == "OB":
                    return self._orderBlock.return_array_list(candles, lookback)
            if pd_type == "Swings":
                    return self._swings.return_array_list(candles, lookback)
            if pd_type == "Void":
                    return self._void.return_array_list(candles, lookback)
            if pd_type == "VI":
                    return self._volume_imbalance.return_array_list(candles, lookback)
        except Exception as e:
            logger.error("Error calculating PD array with lookback: {}".format(e))

    def calculate_pd_array(self, pd_type: str, candles: list[Candle]) -> list:
        """
        Calculate the price delivery (PD) array based on the specified PD type.

        This function analyzes a list of Candle objects and returns a corresponding
        array depending on the specified PD type. The PD types correspond to different
        analytical methods or concepts such as "BPR", "FVG", "BRK", etc. Each PD type
        is processed by its respective method. If an invalid PD type is provided or
        if an error occurs during processing, an error message is logged.

        :param pd_type: The type of price delivery to calculate. Supported values
            include "BPR", "FVG", "BRK", "OB", "RB", "Swings", "Void", "VI".
        :type pd_type: str
        :param candles: A list of Candle objects representing market data for analysis.
        :type candles: list[Candle]
        :return: A list representing the calculated PD array based on the specified
            PD type and the input market data.
        :rtype: list
        """
        try:
            if pd_type == "BPR":
                return self._bpr.return_array_list(candles)
            if pd_type == "FVG":
                return self._fvg.return_array_list(candles)
            if pd_type == "BRK":
                return self._breaker.return_array_list(candles)
            if pd_type == "OB":
                return self._orderBlock.return_array_list(candles)
            if pd_type == "RB":
                return self._rejection_block.return_array_list(candles)
            if pd_type == "Swings":
                return self._swings.return_array_list(candles)
            if pd_type == "Void":
                return self._void.return_array_list(candles)
            if pd_type == "VI":
                return self._volume_imbalance.return_array_list(candles)
        except Exception as e:
            logger.error("Error calculating PD array: {}".format(e))

    def return_candle_range(self, pd_type: str, pdArray: PDArray) -> tuple[float, float]:
        """
        Determines the candle range based on the given price detection (PD) type and price data array.
        This method selects and delegates the computation to the respective handler based on the specified PD type.

        :param pd_type: A string indicating the type of price detection to evaluate. Supported types include
            "BPR", "FVG", "BRK", "OB", "RB", "Swings", "Void", and "VI".
        :param pdArray: The data array containing price detection related information, which is evaluated
            by the relevant handler.
        :return: A tuple containing two floating-point numbers representing the computed range for the input PD type.
        """
        try:
            if pd_type == "BPR":
                return self._bpr.return_candle_range(pdArray)
            if pd_type == "FVG":
                return self._fvg.return_candle_range(pdArray)
            if pd_type == "BRK":
                return self._breaker.return_candle_range(pdArray)
            if pd_type == "OB":
                return self._orderBlock.return_candle_range(pdArray)
            if pd_type == "RB":
                return self._rejection_block.return_candle_range(pdArray)
            if pd_type == "Swings":
                return self._swings.return_candle_range(pdArray)
            if pd_type == "Void":
                return self._void.return_candle_range(pdArray)
            if pd_type == "VI":
                return self._volume_imbalance.return_candle_range(pdArray)
        except Exception as e:
            logger.error(f"PD Candle Range Return Error{e}")

    def check_for_inverse(self, pd_type: str, pdArray: PDArray, candles: list[Candle]) -> str:
        """
        Check for an inverse pattern distribution based on the provided type
        and analyze the given array and candle data.

        This method determines the specific logic to apply for inverse pattern
        detection depending on the `pd_type`. It delegates the inverse check
        to either the `_fvg` or `_orderBlock` attributes or falls back to the
        passed `pdArray` direction if no specific type matches.

        :param pd_type: The type of pattern distribution to check for
                        inversion. Supported values are "FVG" and "OB".
        :type pd_type: str
        :param pdArray: A data structure representing pattern distribution
                        information including direction.
        :type pdArray: PDArray
        :param candles: A list of Candle objects containing price
                        movement data necessary for the inversion check.
        :type candles: list[Candle]
        :return: A string indicating the resulting direction or status of
                 the checked inverse pattern distribution.
        :rtype: str
        :raises Exception: If an unexpected error occurs during the
                           inversion check process.
        """
        try:
            if pd_type == "FVG":
                return self._fvg.checkForInverse(pdArray, candles)
            if pd_type == "OB":
                return self._orderBlock.checkForInverse(pdArray, candles)
            return pdArray.direction
        except Exception as e:
            logger.error(f"PD Inverse check failed{e}")
    # endregion

# todo refactor some enum
