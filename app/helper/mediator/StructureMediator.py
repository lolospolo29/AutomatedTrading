from typing import Any

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.structure.BOS import BOS
from app.models.calculators.frameworks.structure.CISD import CISD
from app.models.calculators.frameworks.structure.Choch import Choch
from app.models.calculators.frameworks.structure.SMT import SMT
from app.monitoring.logging.logging_startup import logger


class StructureMediator:
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
        return self._smt.returnConfirmation(candles_asset1, candles_asset2)
    # endregion
