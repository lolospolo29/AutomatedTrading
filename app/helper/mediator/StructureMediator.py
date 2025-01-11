from typing import Any

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.structure.BOS import BOS
from app.models.calculators.frameworks.structure.CISD import CISD
from app.models.calculators.frameworks.structure.Choch import Choch
from app.models.calculators.frameworks.structure.SMT import SMT


class StructureMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StructureMediator, cls).__new__(cls)
        return cls._instance

    # region Initializing
    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.bos = BOS(10)
            self.choch = Choch(20)
            self.smt = SMT()
            self.cisd = CISD(5)
            self.initialized: bool = True  # Mark as initialized
    # endregion

    # region Analyzing
    def calculateConfirmation(self, confirmationType: str, candles: list[Candle], *args, **kwargs) -> Any:
        if confirmationType == "BOS":
            return self.bos.returnConfirmation(candles)
        if confirmationType == "CHOCH":
            return self.choch.returnConfirmation(candles)
        if confirmationType == "CISD":
            return self.cisd.returnConfirmation(candles)

    def calculateSMT(self,candlesAsset1: list[Candle],candlesAsset2: list[Candle]):
        return self.smt.returnConfirmation(candlesAsset1, candlesAsset2)
    # endregion
