from typing import Any

from Core.Main.Strategy.FrameWorks.Structures.BOS import BOS
from Core.Main.Strategy.FrameWorks.Structures.CISD import CISD
from Core.Main.Strategy.FrameWorks.Structures.Choch import Choch
from Core.Main.Strategy.FrameWorks.Structures.SMT import SMT


class ConfirmationMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfirmationMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.bos = BOS(10)
            self.choch = Choch(20)
            self.smt = SMT()
            self.cisd = CISD(5)
            self.initialized: bool = True  # Mark as initialized

    def calculateConfirmation(self, confirmationType: str, candles: list, *args, **kwargs) -> Any:
        if confirmationType == "BOS":
            return self.bos.returnConfirmation(candles)
        if confirmationType == "CHOCH":
            return self.choch.returnConfirmation(candles)
        if confirmationType == "CISD":
            return self.cisd.returnConfirmation(candles)

        # region SMT should be put as an Extra Strategy implementation & logic
        if confirmationType == "SMT":
            if 'candlesAsset2' in kwargs:
                candlesAsset2 = kwargs['candlesAsset2']
                return self.smt.returnConfirmation(candles, candlesAsset2)
        # endregion
