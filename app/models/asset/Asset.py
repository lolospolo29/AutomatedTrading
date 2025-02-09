from collections import deque
from typing import Optional

from pydantic import BaseModel

from app.models.asset.Candle import Candle
from app.models.asset.Relation import Relation
from app.models.asset.CandleSeries import CandleSeries
from app.models.asset.SMTPair import SMTPair


class Asset(BaseModel):

    name:str
    asset_class:str
    smt_pairs:Optional[list[SMTPair]]
    relations:Optional[list[Relation]]
    candles_series:Optional[list[CandleSeries]]


    def add_relation(self, relation:Relation):
        if self.relations is None:
            self.relations = []
        if relation in self.relations:
            return
        self.relations.append(relation)

    def add_candle(self,candle:Candle):
        for candleSeries in self.candles_series:
            if candleSeries.broker == candle.broker and candleSeries.timeFrame == candle.timeframe:
                candleSeries.add_candle(candle)

    def add_smt_pair(self,smt_pair:SMTPair):
        if self.smt_pairs is None:
            self.smt_pairs = []
        if smt_pair in self.smt_pairs:
            return
        self.smt_pairs.append(smt_pair)

    def add_candles_series(self,_maxlen:int,_timeframe:int,_broker:str):
        for candleSeries_ in self.candles_series:
            if candleSeries_.broker == _broker and candleSeries_.timeFrame == _timeframe:
                return
        self.candles_series.append(CandleSeries(candleSeries=deque(maxlen=_maxlen)
                                                ,timeFrame=_timeframe,broker=_broker))

    def return_relations(self,broker:str)->list[Relation]:
        relations = []
        for relation in self.relations:
            if relation.broker == broker:
                relations.append(relation)
        return relations

    def return_candles(self,timeFrame:int, broker:str)->list[Candle]:
        for candleSeries in self.candles_series:
            if candleSeries.broker == broker and candleSeries.timeFrame == timeFrame:
                return candleSeries.to_list()