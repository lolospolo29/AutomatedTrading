from Models.StrategyAnalyse.PDArrays.BPR import BPR
from Models.StrategyAnalyse.PDArrays.Breaker import Breaker
from Models.StrategyAnalyse.PDArrays.FVG import FVG
from Models.StrategyAnalyse.PDArrays.LiquidityVoid import LiquidityVoid
from Models.StrategyAnalyse.PDArrays.OrderBlock import Orderblock
from Models.StrategyAnalyse.PDArrays.RejectionBlock import RejectionBlock
from Models.StrategyAnalyse.PDArrays.Swings import Swings
from Models.StrategyAnalyse.PDArrays.Void import Void
from Models.StrategyAnalyse.PDArrays.VolumeImbalance import VolumeImbalance


class PDMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PDMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.bpr: BPR = BPR()
            self.fvg = FVG()
            self.breaker: Breaker = Breaker(5)
            self.liquidityVoid: LiquidityVoid = LiquidityVoid(4)
            self.orderBlock: Orderblock = Orderblock()
            self.rejectionBlock: RejectionBlock = RejectionBlock(10)
            self.swings: Swings = Swings()
            self.void: Void = Void()
            self.volumeImbalance: VolumeImbalance = VolumeImbalance()
            self.initialized: bool = True  # Mark as initialized

    def calculatePDArray(self, pdType: str, candles: list) -> list:
        if pdType == "BPR":
            return self.bpr.returnArrayList(candles)
        if pdType == "FVG":
            return self.fvg.returnArrayList(candles)
        if pdType == "BRK":
            return self.breaker.returnArrayList(candles)
        if pdType == "LV":
            return self.liquidityVoid.returnArrayList(candles)
        if pdType == "OB":
            return self.orderBlock.returnArrayList(candles)
        if pdType == "RB":
            return self.rejectionBlock.returnArrayList(candles)
        if pdType == "Swings":
            return self.swings.returnArrayList(candles)
        if pdType == "Void":
            return self.void.returnArrayList(candles)
        if pdType == "VI":
            return self.volumeImbalance.returnArrayList(candles)

