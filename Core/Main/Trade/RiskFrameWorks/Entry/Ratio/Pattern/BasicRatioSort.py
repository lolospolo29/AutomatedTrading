from Core.Main.Trade.OrderDirectionEnum import OrderDirection
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Helper.SortingHelper import SortingHelper
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Pattern.ModeRatioSort import ModeRatioSort
from Core.Main.Trade.RiskFrameWorks.RiskModeEnum import RiskMode


class BasicRatioSort(ModeRatioSort):
    def __init__(self):
        self._SortingHelper = SortingHelper()

    def sort(self,referenceList: list,mode: RiskMode,direction: OrderDirection):
        if mode == RiskMode.AGGRESSIVE:
            if direction == OrderDirection.BUY:
                return self._SortingHelper.returnHighestLevel(referenceList)
            if direction == OrderDirection.SELL:
                return self._SortingHelper.returnLowestLevel(referenceList)
        if mode == RiskMode.MODERAT:
            if direction == OrderDirection.BUY:
                return self._SortingHelper.returnFirstQuartileElementOrFirstOrSecond(referenceList)
            if direction == OrderDirection.SELL:
                return self._SortingHelper.returnThirdQuartileElementOrFirstOrSecond(referenceList)
        if mode == RiskMode.SAFE:
            if direction == OrderDirection.BUY:
                return self._SortingHelper.returnLowestLevel(referenceList)
            if direction == OrderDirection.SELL:
                return self._SortingHelper.returnHighestLevel(referenceList)
