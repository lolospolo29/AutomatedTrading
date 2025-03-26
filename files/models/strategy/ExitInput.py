from pydantic import BaseModel

from files.helper.mediator.PriceMediator import PriceMediator
from files.models.asset.Candle import Candle
from files.models.trade.Trade import Trade


class ExitInput(BaseModel):
    trade:Trade
    candles:list[Candle]
    mediator:PriceMediator