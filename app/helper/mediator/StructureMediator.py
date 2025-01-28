from typing import Any

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.structure.BOS import BOS
from app.models.calculators.frameworks.structure.CISD import CISD
from app.models.calculators.frameworks.structure.Choch import Choch
from app.models.calculators.frameworks.structure.SMT import SMT
from app.monitoring.logging.logging_startup import logger


class StructureMediator:
    """
    Acts as a mediator for structural analysis involving various confirmation
    strategies. It follows the Singleton design pattern to ensure a single
    instance is used across the application. The mediator facilitates calculations
    like BOS (Break of Structure), CHOCH (Change of Character), SMT (Smart Money
    Technique), and CISD (Custom Interval Structure Detection).

    This class initializes the confirmation entities and provides a mechanism to
    perform and retrieve confirmation-specific calculations.

    :ivar _bos: Instance managing the BOS (Break of Structure) calculations with
                a configured parameter, e.g., 10.
    :type _bos: BOS
    :ivar _choch: Instance managing the CHOCH (Change of Character) calculations
                  with a configured parameter, e.g., 20.
    :type _choch: Choch
    :ivar _smt: Instance for managing SMT (Smart Money Technique) calculations.
    :type _smt: SMT
    :ivar _cisd: Instance for managing CISD (Custom Interval Structure Detection)
                 calculations with a configured parameter, e.g., 5.
    :type _cisd: CISD
    :ivar initialized: A boolean flag indicating whether the class has been
                       properly initialized. Prevents re-initialization.
    :type initialized: bool
    """
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StructureMediator, cls).__new__(cls)
        return cls._instance

    # region Initializing
    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self._bos = BOS(10)
            self._choch = Choch(20)
            self._smt = SMT()
            self._cisd = CISD(5)
            self.initialized: bool = True  # Mark as initialized
    # endregion

    # region Analyzing
    def calculate_confirmation(self, confirmation_type: str, candles: list[Candle]) -> Any:
        """
        Calculates and returns a confirmation based on the specified confirmation type
        and a list of candlesticks. The method internally delegates to the appropriate
        confirmation logic based on the confirmation type provided.

        :param confirmation_type: A string specifying the type of confirmation to be
                                  calculated. Supported values include "BOS", "CHOCH",
                                  and "CISD".
        :param candles: A list of candlestick data required for the confirmation
                        calculation. Each element of the list is an instance of the
                        Candle class.
        :return: The result of the confirmation calculation based on the provided type.
                 The type of response depends on the underlying confirmation logic
                 implementation.
        """
        try:
            if confirmation_type == "BOS":
                return self._bos.return_confirmation(candles)
            if confirmation_type == "CHOCH":
                return self._choch.return_confirmation(candles)
            if confirmation_type == "CISD":
                return self._cisd.return_confirmation(candles)
        except Exception as e:
            logger.error(f"Calculate confirmation failed {e}")

    def calculate_smt(self, candles_asset1: list[Candle], candles_asset2: list[Candle]):
        """
        Calculates a specific metric using the provided candle data for two assets. This method computes
        the SMT (Smart Money Technique) by using the candlestick data of two assets and returns a
        confirmation result.

        :param candles_asset1: The list of candlestick objects for asset 1.
        :type candles_asset1: list[Candle]
        :param candles_asset2: The list of candlestick objects for asset 2.
        :type candles_asset2: list[Candle]
        :return: Result of the SMT calculation as a confirmation output.
        :rtype: Confirmation
        """
        return self._smt.returnConfirmation(candles_asset1, candles_asset2)
    # endregion
