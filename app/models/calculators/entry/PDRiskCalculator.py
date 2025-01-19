from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.frameworks.pdarray.BPR import BPR
from app.models.calculators.frameworks.pdarray.Breaker import Breaker
from app.models.calculators.frameworks.pdarray.FVG import FVG
from app.models.calculators.frameworks.pdarray.OrderBlock import Orderblock
from app.models.calculators.frameworks.pdarray.RejectionBlock import RejectionBlock
from app.models.calculators.frameworks.pdarray.Swings import Swings
from app.models.calculators.frameworks.pdarray.Void import Void
from app.models.calculators.frameworks.pdarray.VolumeImbalance import VolumeImbalance
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class PDRiskCalculator:
    """PD Risk Calculator for Profit Stop Entries of the PD Arrays"""

    # region Initializing
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PDRiskCalculator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._bpr: BPR = BPR()
            self._fvg = FVG()
            self._breaker: Breaker = Breaker(5)
            self._orderBlock: Orderblock = Orderblock()
            self._rejection_block: RejectionBlock = RejectionBlock(10)
            self._swings: Swings = Swings()
            self._void: Void = Void()
            self._volume_Imbalance: VolumeImbalance = VolumeImbalance()

            self._initialized: bool = True  # Mark as initialized
    # endregion

    # region Stop Calculation
    def calculate_stop(self, pdArray:PDArray, orderDirection:OrderDirectionEnum, riskMode:RiskMode) -> float:
        try:
            if pdArray.name == "BPR":
                return self._bpr.return_stop(pdArray, orderDirection, riskMode)
            if pdArray.name == "FVG":
                return self._fvg.return_stop(pdArray, orderDirection, riskMode)
            if pdArray.name == "Breaker":
                return self._breaker.return_stop(pdArray, orderDirection, riskMode)
            if pdArray.name == "OB":
                return self._orderBlock.return_stop(pdArray, orderDirection, riskMode)
            if pdArray.name == "RB":
                return self._rejection_block.return_stop(pdArray, orderDirection, riskMode)
            if pdArray.name == "Swings":
                return self._swings.return_stop(pdArray, orderDirection, riskMode)
            if pdArray.name == "Void":
                return self._void.return_stop(pdArray, orderDirection, riskMode)
            if pdArray.name == "VI":
                return self._volume_Imbalance.return_stop(pdArray, orderDirection, riskMode)
        except Exception as e:
            logger.info(f"Calculation failed with exception: {e}")
        finally:
            return -1

    def calculate_stops_specific(self, pdArrays:list[PDArray], orderDirection:OrderDirectionEnum, riskMode:RiskMode) -> list[float]:
        stops = []
        try:
            for pdArray in pdArrays:
                stops.append(self.calculate_stop(pdArray, orderDirection, riskMode))
            return stops
        except Exception as e:
            logger.info("Calculation Exception raised")
        finally:
            return stops

    def calculate_all_stops(self, pdArrays:list[PDArray], orderDirection:OrderDirectionEnum) -> list[float]:

        stops = []
        try:

            riskMode = RiskMode.SAFE

            safeStops = self.calculate_stops_specific(pdArrays, orderDirection, riskMode)

            stops.extend(safeStops)

            riskMode = RiskMode.MODERAT

            moderatStops = self.calculate_stops_specific(pdArrays, orderDirection, riskMode)

            stops.extend(moderatStops)

            riskMode = RiskMode.AGGRESSIVE

            aggressiveStops = self.calculate_stops_specific(pdArrays, orderDirection, riskMode)

            stops.extend(aggressiveStops)
        except Exception as e:
            logger.info("Exception raised while calculating stops")
        finally:
            return stops
    # endregion

    # region Entry Calculation

    def calculate_entry(self, pdArray: PDArray, orderDirection: OrderDirectionEnum, riskMode: RiskMode) -> float:
        try:
            if pdArray.name == "BPR":
                return self._bpr.return_entry(pdArray, orderDirection, riskMode)
            if pdArray.name == "FVG":
                return self._fvg.return_entry(pdArray, orderDirection, riskMode)
            if pdArray.name == "Breaker":
                return self._breaker.return_entry(pdArray, orderDirection, riskMode)
            if pdArray.name == "OB":
                return self._orderBlock.return_entry(pdArray, orderDirection, riskMode)
            if pdArray.name == "RB":
                return self._rejection_block.return_entry(pdArray, orderDirection, riskMode)
            if pdArray.name == "Swings":
                pass
            if pdArray.name == "Void":
                return self._void.return_entry(pdArray, orderDirection, riskMode)
            if pdArray.name == "VI":
                return self._volume_Imbalance.return_entry(pdArray, orderDirection, riskMode)

        except Exception as e:
            logger.info("Exception occurred: {}".format(e))
        finally:
            return -1

    def calculate_entries_specific(self, pdArrays: list[PDArray], orderDirection:
                                   OrderDirectionEnum, riskMode: RiskMode) -> \
                                   list[float]:
        stops = []
        try:
            for pdArray in pdArrays:
                stops.append(self.calculate_entry(pdArray, orderDirection, riskMode))
        except Exception as e:
            logger.info("PD Risk Calculator failed to calculate stops")
        finally:
            return stops

    def calculate_all_entries(self, pdArrays: list[PDArray], orderDirection: OrderDirectionEnum) -> list[float]:

        stops = []

        try:

            riskMode = RiskMode.SAFE

            safeStops = self.calculate_entries_specific(pdArrays, orderDirection, riskMode)

            stops.extend(safeStops)

            riskMode = RiskMode.MODERAT

            moderatStops = self.calculate_entries_specific(pdArrays, orderDirection, riskMode)

            stops.extend(moderatStops)

            riskMode = RiskMode.AGGRESSIVE

            aggressiveStops = self.calculate_entries_specific(pdArrays, orderDirection, riskMode)

            stops.extend(aggressiveStops)
        except Exception as e:
            logger.info("PD Risk Calculator failed to calculate entries due to error")
        finally:
            return stops
    # endregion
