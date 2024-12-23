from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.frameworks.pdarray.BPR import BPR
from app.models.frameworks.pdarray.Breaker import Breaker
from app.models.frameworks.pdarray.FVG import FVG
from app.models.frameworks.pdarray.OrderBlock import Orderblock
from app.models.frameworks.pdarray.RejectionBlock import RejectionBlock
from app.models.frameworks.pdarray.Swings import Swings
from app.models.frameworks.pdarray.Void import Void
from app.models.frameworks.pdarray.VolumeImbalance import VolumeImbalance


class PDMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PDMediator, cls).__new__(cls)
        return cls._instance

    # region Initializing
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
    # endregion

    # region Calculating / Analyzing
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
    # endregion



