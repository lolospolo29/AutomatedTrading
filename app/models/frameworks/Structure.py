from app.models.asset.Candle import Candle
from app.models.frameworks.FrameWork import FrameWork


class Structure(FrameWork):
    candles:list[Candle]
