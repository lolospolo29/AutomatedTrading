from Models.StrategyAnalyse.PDArrays.BPR import BPR
from Models.StrategyAnalyse.PDArrays.Breaker import Breaker
from Models.StrategyAnalyse.PDArrays.LiquidityVoid import LiquidityVoid
from Models.StrategyAnalyse.PDArrays.OrderBlock import Orderblock
from Models.StrategyAnalyse.PDArrays.RejectionBlock import RejectionBlock
from Models.StrategyAnalyse.PDArrays.Swings import Swings
from Models.StrategyAnalyse.PDArrays.Void import Void
from Models.StrategyAnalyse.PDArrays.VolumeImbalance import VolumeImbalance


class CalculatorMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CalculatorMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.bpr: BPR = BPR()
            self.breaker: Breaker = Breaker(10)
            self.liquidityVoid: LiquidityVoid = LiquidityVoid(4)
            self.orderBlock: Orderblock = Orderblock(10)
            self.rejectionBlock: RejectionBlock = RejectionBlock()
            self.swings: Swings = Swings()
            self.void: Void = Void()
            self.volumeImbalance: VolumeImbalance = VolumeImbalance()
            self.initialized: bool = True  # Mark as initialized

    def calculatePDArray(self,calculatorType: str, candles: list):
        if calculatorType == "BPR":
            self.bpr.getArrayList(candles)
        if calculatorType == "Breaker":
            self.breaker.getArrayList(candles)
        if calculatorType == "LiquidityVoid":
            self.liquidityVoid.getArrayList(candles)
        if calculatorType == "RejectionBlock":
            self.rejectionBlock.getArrayList(candles)
        if calculatorType == "Swings":
            self.swings.getArrayList(candles)
        if calculatorType == "Void":
            self.void.getArrayList(candles)
        if calculatorType == "VolumeImbalance":
            self.volumeImbalance.getArrayList(candles)

