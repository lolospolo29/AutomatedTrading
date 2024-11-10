from typing import Any

from Models.StrategyAnalyse.Confirmation.BOS import BOS
from Models.StrategyAnalyse.Confirmation.Choch import Choch
from Models.StrategyAnalyse.Confirmation.SMT import SMT


class ConfirmationMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfirmationMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.bos = BOS(10)
            self.choch = Choch(10)
            self.smt = SMT()
            self.initialized: bool = True  # Mark as initialized

    def calculateConfirmation(self, confirmationType: str, candles: list, *args, **kwargs) -> Any:
        if confirmationType == "BOS":
            return self.bos.returnConfirmation(candles)
        if confirmationType == "Choch":
            return self.choch.returnConfirmation(candles)
        if confirmationType == "SMT":
            if 'candlesAsset2' in kwargs:
                candlesAsset2 = kwargs['candlesAsset2']
                return self.smt.returnConfirmation(candles, candlesAsset2)

