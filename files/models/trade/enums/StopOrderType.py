from enum import Enum


class StopOrderType(Enum):
    TakeProfit = "TakeProfit"
    StopLoss = "StopLoss"
    TrailingStop = "TrailingStop"
    Stop = "Stop"
    PartialTakeProfit = "PartialTakeProfit"
    PartialStopLoss = "PartialStopLoss"
    tpslOrder = "tpslOrder"
    OcoOrder = "OcoOrder"
    MmRateClose = "MmRateClose"