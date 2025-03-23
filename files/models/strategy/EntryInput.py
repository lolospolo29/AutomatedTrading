from files.helper.mediator.PriceMediator import PriceMediator
from files.models.asset.Candle import Candle


class EntryInput:
    candles:list[Candle]
    price_mediator:PriceMediator