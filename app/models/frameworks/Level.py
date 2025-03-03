from app.models.asset.Candle import Candle
from app.models.frameworks.FrameWork import FrameWork


class Level(FrameWork):
    level:float
    fib_level:float
    candles:list[Candle]