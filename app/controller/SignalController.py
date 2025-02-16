from typing import Dict, Any

from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.manager.AssetManager import AssetManager
from app.manager.RelationManager import RelationManager
from app.manager.StrategyManager import StrategyManager
from app.manager.TradeManager import TradeManager
from app.models.asset.Asset import Asset
from app.models.asset.Relation import Relation
from app.monitoring.logging.logging_startup import logger
from app.services.TradingService import TradingService


class SignalController:

    # region Initializing
    def __init__(self):
        self._TradingService: TradingService = TradingService()
        self._TradeManager = TradeManager()
        self._AssetManager = AssetManager()
        self._relation_manager = RelationManager()
        self._StrategyManager = StrategyManager()
    # endregion

    def get_trades(self)->list[dict]:
        trades = self._TradeManager.return_trades()
        updated_trades = []
        for trade in trades:
            try:
                trade_str:dict = trade.dict()
                updated_trades.append(trade_str)
            except Exception as e:
                logger.error("Error appending trade to list: {id},Error:{e}".format(id=trade.id,e=e))
        return updated_trades

    def update_trade(self):
        pass

    def add_trade(self):
        pass

    def delete_trade(self):
        pass

    def get_smt_pairs(self)->list[dict]:
        pass

    def add_smt_pair(self):
        pass

    def update_smt_pair(self):
        pass

    def delete_smt_pair(self):
        pass

    def get_relations(self)->list[dict]:
        pass

    def add_relation(self,json_data:Dict[str,Any] = None):
        try:
            relation = Relation.model_validate(json_data)
            self._relation_manager.create_relation(relation=relation)
        except Exception as e:
            logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def update_relation(self):
        pass

    def delete_relation(self):
        pass

    def get_assets(self)->list[dict]:
        assets = self._AssetManager.return_all_assets()
        dict_assets = []
        for asset in assets:
            try:
                asset_dict:dict = asset.dict(exclude={'candles_series'})
                dict_assets.append(asset_dict)
            except Exception as e:
                logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=asset.name,e=e))
        return dict_assets

    def add_asset(self, json_data: Dict[str, Any]) -> None:
        try:
            self._AssetManager.create_asset(Asset.model_validate(json_data))
        except Exception as e:
            logger.warning("Price Action Signal failed,Error: {e}".format(e=e))

    def update_asset(self, json_data: Dict[str, Any]):
        try:
            self._AssetManager.update_asset(Asset.model_validate(json_data))
        except Exception as e:
            logger.warning("Price Action Signal failed,Error: {e}".format(e=e))

    def delete_asset(self,json_data:Dict[str,Any] = None):
        try:
            asset = Asset.model_validate(json_data)
            self._AssetManager.delete_asset(asset)
        except Exception as e:
            logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def get_strategies(self):
        strategies = self._StrategyManager.return_strategies()
        dict_strategies = []
        for strategy in strategies:
            try:
                strategy_dict: dict = strategy.dict(exclude={"time_windows", "strategy_facade"})
                dict_strategies.append(strategy_dict)
            except Exception as e:
                logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=strategy.name, e=e))
        return dict_strategies

    def get_brokers(self):
        brokers:list[BrokerDTO] = self._TradeManager.get_brokers()
        dict_brokers = []
        for broker in brokers:
            try:
                broker_dict:dict = broker.dict(exclude={"id"})
                dict_brokers.append(broker_dict)
            except Exception as e:
                logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=broker.name,e=e))
        return dict_brokers

    # region TradingView Handling
    def trading_view_signal(self, json_data: Dict[str, Any]) -> None:
        try:
            self._TradingService.handle_price_action_signal(json_data)
        except Exception as e:
            logger.warning("Price Action Signal failed,Error: {e}".format(e=e))
    # endregion
