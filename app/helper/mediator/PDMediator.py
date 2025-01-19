from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.frameworks.pdarray.BPR import BPR
from app.models.calculators.frameworks.pdarray.Breaker import Breaker
from app.models.calculators.frameworks.pdarray.FVG import FVG
from app.models.calculators.frameworks.pdarray.OrderBlock import Orderblock
from app.models.calculators.frameworks.pdarray.RejectionBlock import RejectionBlock
from app.models.calculators.frameworks.pdarray.Swings import Swings
from app.models.calculators.frameworks.pdarray.Void import Void
from app.models.calculators.frameworks.pdarray.VolumeImbalance import VolumeImbalance
from app.monitoring.logging.logging_startup import logger


class PDMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PDMediator, cls).__new__(cls)
        return cls._instance

    # region Initializing
    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self._bpr: BPR = BPR()
            self._fvg = FVG()
            self._breaker: Breaker = Breaker(5)
            self._orderBlock: Orderblock = Orderblock()
            self._rejection_block: RejectionBlock = RejectionBlock(10)
            self._swings: Swings = Swings()
            self._void: Void = Void()
            self._volume_imbalance: VolumeImbalance = VolumeImbalance()
            self.initialized: bool = True  # Mark as initialized
    # endregion

    # region Calculating / Analyzing
    def calculate_pd_array_with_lookback(self, pd_type: str, candles: list[Candle], lookback) -> list:
        try:
            if pd_type == "FVG":
                    return self._fvg.return_array_list(candles, lookback)
            if pd_type == "OB":
                    return self._orderBlock.return_array_list(candles, lookback)
            if pd_type == "Swings":
                    return self._swings.return_array_list(candles, lookback)
            if pd_type == "Void":
                    return self._void.return_array_list(candles, lookback)
            if pd_type == "VI":
                    return self._volume_imbalance.return_array_list(candles, lookback)
        except Exception as e:
            logger.error("Calculate PD array with type {} failed.".format(pd_type))

    def calculate_pd_array(self, pd_type: str, candles: list[Candle]) -> list:
        try:
            if pd_type == "BPR":
                return self._bpr.return_array_list(candles)
            if pd_type == "FVG":
                return self._fvg.return_array_list(candles)
            if pd_type == "BRK":
                return self._breaker.return_array_list(candles)
            if pd_type == "OB":
                return self._orderBlock.return_array_list(candles)
            if pd_type == "RB":
                return self._rejection_block.return_array_list(candles)
            if pd_type == "Swings":
                return self._swings.return_array_list(candles)
            if pd_type == "Void":
                return self._void.return_array_list(candles)
            if pd_type == "VI":
                return self._volume_imbalance.return_array_list(candles)
        except Exception as e:
            logger.error("Error calculating PD array: {}".format(e))

    def return_candle_range(self, pd_type: str, pdArray: PDArray) -> tuple[float, float]:
        try:
            if pd_type == "BPR":
                return self._bpr.return_candle_range(pdArray)
            if pd_type == "FVG":
                return self._fvg.return_candle_range(pdArray)
            if pd_type == "BRK":
                return self._breaker.return_candle_range(pdArray)
            if pd_type == "OB":
                return self._orderBlock.return_candle_range(pdArray)
            if pd_type == "RB":
                return self._rejection_block.return_candle_range(pdArray)
            if pd_type == "Swings":
                return self._swings.return_candle_range(pdArray)
            if pd_type == "Void":
                return self._void.return_candle_range(pdArray)
            if pd_type == "VI":
                return self._volume_imbalance.return_candle_range(pdArray)
        except Exception as e:
            logger.error(f"PD Candle Range Return Error{e}")

    def check_for_inverse(self, pd_type: str, pdArray: PDArray, candles: list[Candle]) -> str:
        try:
            if pd_type == "FVG":
                return self._fvg.checkForInverse(pdArray, candles)
            if pd_type == "OB":
                return self._orderBlock.checkForInverse(pdArray, candles)
            return pdArray.direction
        except Exception as e:
            logger.error(f"PD Inverse check failed{e}")
    # endregion



