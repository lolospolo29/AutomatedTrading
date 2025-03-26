import uuid
from collections import deque
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel,Field

from files.models.asset.Candle import Candle
from files.models.asset.CandleSeries import CandleSeries
from files.models.PyObjectId import PyObjectId


class Asset(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")

    asset_id: int = Field(alias="assetId",default_factory=lambda: uuid.uuid4().__str__())
    name: str
    asset_class_id: int = Field(alias="assetClassId")
    candles_series: Optional[list['CandleSeries']] = Field(exclude=True,default=None)

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated

    def add_candle(self,candle:Candle):
        for candleSeries in self.candles_series:
            if candleSeries.broker_id == candle.broker and candleSeries.time_frame == candle.timeframe:
                candleSeries.add_candle(candle)
                return
        self.add_candles_series(candle.timeFrame, candle.broker)
        self.add_candle(candle)

    def add_candles_series(self,timeframe:int, _broker:str):
        if timeframe > 5:
            self.candles_series.append(CandleSeries(candle_series=deque(maxlen=240)
                                                    , time_frame=timeframe, broker=_broker))
        if timeframe == 5:
            self.candles_series.append(CandleSeries(candle_series=deque(maxlen=150)
                                                    , time_frame=timeframe, broker=_broker))
        if 15 < timeframe < 240:
            self.candles_series.append(CandleSeries(candle_series=deque(maxlen=336)
                                                    , time_frame=timeframe, broker=_broker))
        if timeframe == 240:
            self.candles_series.append(CandleSeries(candle_series=deque(maxlen=168)
                                                    , time_frame=timeframe, broker=_broker))
        if timeframe == 1440:
            self.candles_series.append(CandleSeries(candle_series=deque(maxlen=120)
                                                    , time_frame=timeframe, broker=_broker))

    def return_candles(self, time_frame:int, broker:str)->list[Candle]:
        for candle_series in self.candles_series:
            candle_series:CandleSeries
            if candle_series.broker == broker and candle_series.time_frame == time_frame:
                return list(candle_series.candle_series)

    def update_asset(self,asset: 'Asset'):
        self.asset_class_id = asset.asset_class_id