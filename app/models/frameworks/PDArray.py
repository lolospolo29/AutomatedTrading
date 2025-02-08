from app.models.asset.Candle import Candle
from app.models.frameworks.FrameWork import FrameWork


class PDArray(FrameWork):
    candles:list[Candle]
    status:str="Normal"
