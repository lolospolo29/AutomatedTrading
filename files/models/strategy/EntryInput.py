from pydantic import BaseModel

from files.helper.mediator.PriceMediator import PriceMediator
from files.models.asset.Candle import Candle


class EntryInput(BaseModel):
    candles:list[Candle]
    price_mediator:PriceMediator