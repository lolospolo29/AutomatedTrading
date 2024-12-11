from Core.StrategyAnalyse.PDArray import PDArray
from Core.StrategyAnalyse.PDArrays.BPR import BPR
from Core.StrategyAnalyse.PDArrays.Breaker import Breaker
from Core.StrategyAnalyse.PDArrays.FVG import FVG
from Core.StrategyAnalyse.PDArrays.OrderBlock import Orderblock
from Core.StrategyAnalyse.PDArrays.RejectionBlock import RejectionBlock
from Core.StrategyAnalyse.PDArrays.Swings import Swings
from Core.StrategyAnalyse.PDArrays.Void import Void
from Core.StrategyAnalyse.PDArrays.VolumeImbalance import VolumeImbalance


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
            self.orderBlock: Orderblock = Orderblock()
            self.rejectionBlock: RejectionBlock = RejectionBlock(10)
            self.swings: Swings = Swings()
            self.void: Void = Void()
            self.volumeImbalance: VolumeImbalance = VolumeImbalance()
            self.initialized: bool = True  # Mark as initialized

    def calculatePDArray(self, pdType: str, candles: list, *args, **kwargs) -> list:
        if pdType == "BPR":
            return self.bpr.returnArrayList(candles)
        if pdType == "FVG":
            if 'lookback' in kwargs:
                lookback = kwargs['lookback']
                return self.fvg.returnArrayList(candles,lookback)
            return self.fvg.returnArrayList(candles)
        if pdType == "BRK":
            return self.breaker.returnArrayList(candles)
        if pdType == "OB":
            if 'lookback' in kwargs:
                lookback = kwargs['lookback']
                return self.orderBlock.returnArrayList(candles,lookback)
            return self.orderBlock.returnArrayList(candles)
        if pdType == "RB":
            return self.rejectionBlock.returnArrayList(candles)
        if pdType == "Swings":
            if 'lookback' in kwargs:
                lookback = kwargs['lookback']
                return self.swings.returnArrayList(candles,lookback)
            return self.swings.returnArrayList(candles)
        if pdType == "Void":
            if 'lookback' in kwargs:
                lookback = kwargs['lookback']
                return self.void.returnArrayList(candles,lookback)
            return self.void.returnArrayList(candles)
        if pdType == "VI":
            if 'lookback' in kwargs:
                lookback = kwargs['lookback']
                return self.volumeImbalance.returnArrayList(candles,lookback)
            return self.volumeImbalance.returnArrayList(candles)

    def returnCandleRange(self,pdType: str, pdArray: PDArray) -> dict:
        if pdType == "BPR":
            return self.bpr.returnCandleRange(pdArray)
        if pdType == "FVG":
            return self.fvg.returnCandleRange(pdArray)
        if pdType == "BRK":
            return self.breaker.returnCandleRange(pdArray)
        if pdType == "OB":
            return self.orderBlock.returnCandleRange(pdArray)
        if pdType == "RB":
            return self.rejectionBlock.returnCandleRange(pdArray)
        if pdType == "Swings":
            return self.swings.returnCandleRange(pdArray)
        if pdType == "Void":
            return self.void.returnCandleRange(pdArray)
        if pdType == "VI":
            return self.volumeImbalance.returnCandleRange(pdArray)

    def checkForInverse(self,pdType: str, pdArray: PDArray, candles: list) -> str:
        if pdType == "FVG":
            return self.fvg.checkForInverse(pdArray, candles)
        if pdType == "OB":
            return self.orderBlock.checkForInverse(pdArray, candles)
        return pdArray.direction



