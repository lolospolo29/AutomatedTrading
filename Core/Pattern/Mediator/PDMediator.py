from Core.Main.Asset.SubModels.Candle import Candle
from Core.Main.Strategy.FrameWorks.PDArray import PDArray
from Core.Main.Strategy.FrameWorks.PDArrays.BPR import BPR
from Core.Main.Strategy.FrameWorks.PDArrays.Breaker import Breaker
from Core.Main.Strategy.FrameWorks.PDArrays.FVG import FVG
from Core.Main.Strategy.FrameWorks.PDArrays.OrderBlock import Orderblock
from Core.Main.Strategy.FrameWorks.PDArrays.RejectionBlock import RejectionBlock
from Core.Main.Strategy.FrameWorks.PDArrays.Swings import Swings
from Core.Main.Strategy.FrameWorks.PDArrays.Void import Void
from Core.Main.Strategy.FrameWorks.PDArrays.VolumeImbalance import VolumeImbalance


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

    def calculatePDArrayWithLookback(self,pdType: str, candles: list[Candle],lookback) -> list:
        if pdType == "FVG":
                return self.fvg.returnArrayList(candles,lookback)
        if pdType == "OB":
                return self.orderBlock.returnArrayList(candles,lookback)
        if pdType == "Swings":
                return self.swings.returnArrayList(candles,lookback)
        if pdType == "Void":
                return self.void.returnArrayList(candles,lookback)
        if pdType == "VI":
                return self.volumeImbalance.returnArrayList(candles,lookback)

    def calculatePDArray(self, pdType: str, candles: list[Candle]) -> list:
        if pdType == "BPR":
            return self.bpr.returnArrayList(candles)
        if pdType == "FVG":
            return self.fvg.returnArrayList(candles)
        if pdType == "BRK":
            return self.breaker.returnArrayList(candles)
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

    def checkForInverse(self,pdType: str, pdArray: PDArray, candles: list[Candle]) -> str:
        if pdType == "FVG":
            return self.fvg.checkForInverse(pdArray, candles)
        if pdType == "OB":
            return self.orderBlock.checkForInverse(pdArray, candles)
        return pdArray.direction



