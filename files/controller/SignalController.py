from logging import Logger
from typing import Dict, Any

from files.models.trade.Broker import Broker
from files.models.asset.Category import Category
from files.helper.manager.RelationManager import RelationManager
from files.helper.manager.SMTManager import SMTManager
from files.models.asset.Relation import Relation
from files.models.asset.SMTPair import SMTPair
from files.services.BrokerService import BrokerService
from files.services.TradingService import TradingService

class SignalController:

    # region Initializing
    def __init__(self, trading_service:TradingService, broker_service:BrokerService
                 , relation_manager:RelationManager, logger:Logger, smt_manager:SMTManager):
        self._TradingService: TradingService = trading_service
        self._BrokerService = broker_service
        self._Relation_manager = relation_manager
        self._SMT_manager = smt_manager
        self._logger = logger
    # endregion

    def get_trades(self)->list[dict]:
        trades = self._BrokerService.return_storage_trades()
        updated_trades = []
        for trade in trades:
            try:
                trade_str:dict = trade.dict()
                updated_trades.append(trade_str)
            except Exception as e:
                self._logger.error("Error appending trade to list: {id},Error:{e}".format(id=trade.id,e=e))
                continue
        return updated_trades

    def get_brokers(self):
        brokers:list[Broker] = self._BrokerService.get_brokers()
        dict_brokers = []
        for broker in brokers:
            try:
                broker_dict:dict = broker.dict(exclude={"id"})
                dict_brokers.append(broker_dict)
            except Exception as e:
                self._logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=broker._name, e=e))
                continue
        return dict_brokers

    def get_smt_pairs(self)->list[dict]:
        smt_pairs:list[SMTPair] = self._SMT_manager.return_smt_pairs()
        dict_smt_pairs = []
        for smt_pair in smt_pairs:
            try:
                relation_dict:dict = smt_pair.dict()
                dict_smt_pairs.append(relation_dict)
            except Exception as e:
                self._logger.error("Error appending relation to list: {id},Error:{e}".format(id=smt_pair.strategy,e=e))
                continue
        return dict_smt_pairs

    def add_smt_pair(self,json_data:Dict[str,Any] = None):
        try:
            smt_pair = SMTPair.model_validate(json_data)
            self._SMT_manager.create_smt(smt_pair)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def add_relation(self,json_data:Dict[str,Any] = None):
        try:
            relation = Relation.model_validate(json_data)
            self._Relation_manager.create_relation(relation=relation)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def get_relations(self)->list[dict]:
        relations:list[Relation] = self._Relation_manager.return_relations()
        dict_relations = []
        for relation in relations:
            try:
                relation_dict:dict = relation.dict()
                dict_relations.append(relation_dict)
            except Exception as e:
                self._logger.error("Error appending relation to list: {id},Error:{e}".format(id=relation.id,e=e))
                continue
        return dict_relations

    def get_categories(self):
        categories:list[Category] = self._Relation_manager.return_categories()
        dict_categories = []
        for category in categories:
            try:
                category_dict:dict = category.dict(exclude={"id"})
                dict_categories.append(category_dict)
            except Exception as e:
                self._logger.error("Error while dumping category name: {name},Error:{e}".format(name=category._name, e=e))
                continue
        return dict_categories

    def update_relation(self,json_data:Dict[str,Any] = None):
        try:
            self._Relation_manager.update_relation(Relation.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Update Relation failed,Error: {e}".format(e=e))

    def delete_relation(self,json_data:Dict[str,Any] = None):
        try:
            self._Relation_manager.delete_relation(Relation.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Delete Relation failed,Error: {e}".format(e=e))

    # region TradingView Handling
    def trading_view_signal(self, json_data: Dict[str, Any]) -> None:
        try:
            self._TradingService.handle_price_action_signal(json_data)
        except Exception as e:
            self._logger.warning("Price Action Signal failed,Error: {e}".format(e=e))


    def atr_signal(self, json_data: Dict[str, Any]):
        try:
            self._TradingService.handle_price_action_signal(json_data)
        except Exception as e:
            self._logger.warning("ATR Signal failed,Error: {e}".format(e=e))
    # endregion
