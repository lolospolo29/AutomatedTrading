from dataclasses import dataclass, field
from typing import Optional

from numpy import long

@dataclass
class Positions:

    positionIdx: Optional[int] = field(default=None)
    riskId: Optional[str] = field(default=None)
    riskLimitValue: Optional[str] = field(default=None)
    symbol: Optional[str] = field(default=None)
    side: Optional[str] = field(default=None)
    size: Optional[str] = field(default=None)
    avgPrice: Optional[str] = field(default=None)
    positionValue: Optional[str] = field(default=None)
    tradeMode: Optional[int] = field(default=None)
    autoAddMargin: Optional[int] = field(default=None)
    positionStatus: Optional[str] = field(default=None)
    leverage: Optional[str] = field(default=None)
    markPrice: Optional[str] = field(default=None)
    liqPrice: Optional[str] = field(default=None)
    bustPrice: Optional[str] = field(default=None)
    positionMM: Optional[str] = field(default=None)
    positionBalance: Optional[str] = field(default=None)
    takeProfit: Optional[str] = field(default=None)
    stopLoss: Optional[str] = field(default=None)
    trailingStop: Optional[str] = field(default=None)
    sessionAvgPrice: Optional[str] = field(default=None)
    delta: Optional[str] = field(default=None)
    gamma: Optional[str] = field(default=None)
    vega: Optional[str] = field(default=None)
    theta: Optional[str] = field(default=None)
    unrealisedPnl: Optional[str] = field(default=None)
    curRealisedPnl: Optional[str] = field(default=None)
    cumRealisedPnl: Optional[str] = field(default=None)
    adlRankIndicator: Optional[int] = field(default=None)
    createdTIme: Optional[int] = field(default=None)
    updatedTime: Optional[int] = field(default=None)
    seq: Optional[long] = field(default=None)
    isReduceOnly: Optional[bool] = field(default=None)
    mmrSysUpdatedTime: Optional[str] = field(default=None)
    leverageSysUpdatedTime: Optional[str] = field(default=None)
    tpslMode: Optional[str] = field(default=None)
