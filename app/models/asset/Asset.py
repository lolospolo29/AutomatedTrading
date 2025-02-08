from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.asset.CandleSeries import CandleSeries
from app.models.asset.SMTPair import SMTPair


class Asset:

    # region Initializing
    def __init__(self, name: str, asset_class:str):
        self.name: str = name
        self.asset_class:str = asset_class
        self.brokers: list[str] = []
        self.strategies: list[str] = []
        self.smt_pairs: list[SMTPair] = []
        self.relations: list[AssetBrokerStrategyRelation] = []
        self.candles_series: list[CandleSeries] = []
    # endregion

    # region Add Functions
    def add_broker(self, broker: str) -> bool:
        if not self._is_broker_in_brokers(broker):
            self.brokers.append(broker)
            return True
        return False

    def add_strategy(self, strategy: str) -> bool:
        if not self._is_strategy_in_strategies(strategy):
            self.strategies.append(strategy)
            return True
        return False

    def add_smt_pair(self, pair: SMTPair) -> bool:
        if not self._is_pair_in_smt_pairs(pair):
            self.smt_pairs.append(pair)
            return True
        return False

    def add_candle_series(self, time_frame: int, maxlen: int, broker: str) -> bool:
        for candle_series in self.candles_series:
            if not self._is_broker_and_time_frame_in_candle_series(broker, time_frame, candle_series):
                self.candles_series.append(CandleSeries(time_frame, maxlen, broker))
                return True
        if len(self.candles_series) == 0:
            if self._is_broker_in_brokers(broker):
                self.candles_series.append(CandleSeries(time_frame, maxlen, broker))
                return True
            return False

    def add_relation(self, relation:AssetBrokerStrategyRelation) -> bool:
            if not self._is_relation_in_relations(relation.broker, relation.strategy):
                if self._is_broker_in_brokers(relation.broker) and self._is_strategy_in_strategies(relation.strategy):
                    self.relations.append(relation)
                    return True
            return False

    def add_candle(self, candle: Candle) -> bool:
        for candleSeries in self.candles_series:
            if self._is_broker_and_time_frame_in_candle_series(candle.broker, candle.timeframe, candleSeries):
                candleSeries.add_candle(candle)
                return True
    # endregion

    # region Return Functions
    def return_candles(self, time_frame: int, broker: str) -> list[Candle]:
        for series in self.candles_series:
            if self._is_broker_and_time_frame_in_candle_series(broker, time_frame, series):
                return series.to_list()
        return []

    def return_candle_series(self) -> list[CandleSeries]:
        allSeries = []
        for series in self.candles_series:
            allSeries.append(series)
        return allSeries

    def return_smt_pair(self, pairName: str)-> SMTPair:
        for smtPair in self.smt_pairs:
            for pair in smtPair.smt_pairs:
                if pair == pairName:
                    return smtPair

    def return_relations_for_broker(self, broker: str) -> list[AssetBrokerStrategyRelation]:
        relations: list[AssetBrokerStrategyRelation] = []
        for assignment in self.relations:
            if broker == assignment.broker:
                relations.append(assignment)
        return relations#

    def to_dict(self) -> dict:
        return {
                "name": self.name,
                "asset_class": self.asset_class,
                "brokers": self.brokers,
                "strategies": self.strategies,
                "smt_pairs": [pair.to_dict() for pair in self.smt_pairs],
                "relations": [relation.to_dict() for relation in self.relations]
        }
    # endregion

    # region Checking
    def _is_broker_in_brokers(self, broker: str) -> bool:
        if broker in self.brokers:
            return True
        return False

    def _is_strategy_in_strategies(self, strategy: str) -> bool:
        if strategy in self.strategies:
            return True
        return False

    def _is_pair_in_smt_pairs(self, pair: SMTPair) -> bool:
        for existingPair in self.smt_pairs:
            if (existingPair.strategy == pair.strategy and
                    existingPair.correlation == pair.correlation and
                    sorted(existingPair.smt_pairs) == sorted(
                        pair.smt_pairs)):  # Ensure elements match, regardless of order
                return True
        return False

    @staticmethod
    def _is_broker_and_time_frame_in_candle_series(broker: str, timeFrame: int, candle_series: CandleSeries)-> bool:
        if candle_series.broker == broker and candle_series.timeFrame == timeFrame:
            return True
        return False

    def _is_relation_in_relations(self, broker: str, strategy: str) -> bool:
        for relation in self.relations:
            if relation.strategy == strategy and relation.broker == broker:
                return True
        return False
    # endregion


