from collections import deque
from typing import Optional

from pydantic import BaseModel

from files.models.asset.Candle import Candle
from files.models.asset.Relation import Relation
from files.models.asset.CandleSeries import CandleSeries
from files.models.asset.SMTPair import SMTPair


class Asset(BaseModel):
    asset_id: int
    name: str
    asset_class: str
    smt_pairs: Optional[list['SMTPair']] = None  # Can be None
    relations: Optional[list['Relation']] = None  # Can be None
    candles_series: Optional[list['CandleSeries']] = None  # Can be None

    def update_asset(self,asset:'Asset'):
        if asset.smt_pairs is not None:
            self.smt_pairs = asset.smt_pairs
        if asset.relations is not None:
            self.relations = asset.relations

    def remove_relation(self, relation:Relation):
        if self.relations is None:
            return
        self.relations.remove(relation)

        candles_series = self.candles_series.copy()

        for candleSeries in candles_series:
            if candleSeries.broker == relation.broker:
                self.candles_series.remove(candleSeries)
        smt_pairs = self.smt_pairs
        for smt_pair in smt_pairs:
            if smt_pair.broker == relation.broker and (smt_pair.asset_1 == relation.asset_1 or smt_pair.asset_2 == relation.asset_1):
                self.smt_pairs.remove(smt_pair)

    def update_relation(self,relation:Relation):
        relations = self.relations.copy()
        for relation_ in relations:
            if relation_.id == relation.id:
                self.relations.remove(relation_)
                self.relations.append(relation)
                return

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
