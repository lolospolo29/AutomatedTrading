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
from app.models.trade.enums.OrderDirectionEnum import OrderDirection


class PDRiskCalculator:

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
            self._rejectionBlock: RejectionBlock = RejectionBlock(10)
            self._swings: Swings = Swings()
            self._void: Void = Void()
            self._volumeImbalance: VolumeImbalance = VolumeImbalance()

            self._initialized: bool = True  # Mark as initialized
    # endregion

    # region Stop Calculation
    def calculateStop(self, pdArray:PDArray, orderDirection:OrderDirection, riskMode:RiskMode) -> float:
        if pdArray.name == "BPR":
            return self._bpr.returnStop(pdArray,orderDirection,riskMode)
        if pdArray.name == "FVG":
            return self._fvg.returnStop(pdArray,orderDirection,riskMode)
        if pdArray.name == "Breaker":
            return self._breaker.returnStop(pdArray,orderDirection,riskMode)
        if pdArray.name == "OB":
            return self._orderBlock.returnStop(pdArray,orderDirection,riskMode)
        if pdArray.name == "RB":
            return self._rejectionBlock.returnStop(pdArray,orderDirection,riskMode)
        if pdArray.name == "Swings":
            return self._swings.returnStop(pdArray,orderDirection,riskMode)
        if pdArray.name == "Void":
            return self._void.returnStop(pdArray,orderDirection,riskMode)
        if pdArray.name == "VI":
            return self._volumeImbalance.returnStop(pdArray,orderDirection,riskMode)

    def calculateStopsSpecific(self,pdArrays:list[PDArray],orderDirection:OrderDirection,riskMode:RiskMode) -> list[float]:
        stops = []
        for pdArray in pdArrays:
            stops.append(self.calculateStop(pdArray, orderDirection, riskMode))
        return stops

    def calculateAllStops(self,pdArrays:list[PDArray],orderDirection:OrderDirection) -> list[float]:

        stops = []

        riskMode = RiskMode.SAFE

        safeStops = self.calculateStopsSpecific(pdArrays,orderDirection,riskMode)

        stops.extend(safeStops)

        riskMode = RiskMode.MODERAT

        moderatStops = self.calculateStopsSpecific(pdArrays,orderDirection,riskMode)

        stops.extend(moderatStops)

        riskMode = RiskMode.AGGRESSIVE

        aggressiveStops = self.calculateStopsSpecific(pdArrays,orderDirection,riskMode)

        stops.extend(aggressiveStops)

        return stops
    # endregion

    # region Entry Calculation
    def calculateEntry(self, pdArray: PDArray, orderDirection: OrderDirection, riskMode: RiskMode) -> float:
        if pdArray.name == "BPR":
            return self._bpr.returnEntry(pdArray, orderDirection, riskMode)
        if pdArray.name == "FVG":
            return self._fvg.returnEntry(pdArray, orderDirection, riskMode)
        if pdArray.name == "Breaker":
            return self._breaker.returnEntry(pdArray, orderDirection, riskMode)
        if pdArray.name == "OB":
            return self._orderBlock.returnEntry(pdArray, orderDirection, riskMode)
        if pdArray.name == "RB":
            return self._rejectionBlock.returnEntry(pdArray, orderDirection, riskMode)
        if pdArray.name == "Swings":
            pass
        if pdArray.name == "Void":
            return self._void.returnEntry(pdArray, orderDirection, riskMode)
        if pdArray.name == "VI":
            return self._volumeImbalance.returnEntry(pdArray, orderDirection, riskMode)

    def calculateEntriesSpecific(self, pdArrays: list[PDArray], orderDirection: OrderDirection, riskMode: RiskMode) -> \
    list[float]:
        stops = []
        for pdArray in pdArrays:
            stops.append(self.calculateEntry(pdArray, orderDirection, riskMode))
        return stops

    def calculateAllEntries(self, pdArrays: list[PDArray], orderDirection: OrderDirection) -> list[float]:

        stops = []

        riskMode = RiskMode.SAFE

        safeStops = self.calculateEntriesSpecific(pdArrays, orderDirection, riskMode)

        stops.extend(safeStops)

        riskMode = RiskMode.MODERAT

        moderatStops = self.calculateEntriesSpecific(pdArrays, orderDirection, riskMode)

        stops.extend(moderatStops)

        riskMode = RiskMode.AGGRESSIVE

        aggressiveStops = self.calculateEntriesSpecific(pdArrays, orderDirection, riskMode)

        stops.extend(aggressiveStops)

        return stops
    # endregion
