from logging import Logger
from typing import Dict, Any

from files.db.mongodb.dtos.AssetClassDTO import AssetClassDTO
from files.db.mongodb.dtos.BrokerDTO import BrokerDTO
from files.db.mongodb.dtos.CategoryDTO import CategoryDTO
from files.helper.manager.AssetManager import AssetManager
from files.helper.manager.RelationManager import RelationManager
from files.helper.registry.StrategyRegistry import StrategyRegistry
from files.helper.manager.TradeManager import TradeManager
from files.models.asset.Asset import Asset
from files.models.asset.Relation import Relation
from files.models.asset.SMTPair import SMTPair
from files.models.backtest.BacktestInput import BacktestInput
from files.services.BacktestService import BacktestService
from files.services.NewsService import NewsService
from files.services.TradingService import TradingService
from tools.EconomicScrapper.Models.NewsDay import NewsDay


class SignalController:

    # region Initializing
    def __init__(self,trading_service:TradingService, news_service:NewsService,asset_manager:AssetManager, trade_manager:TradeManager
                 ,relation_manager:RelationManager,backtest_service:BacktestService,logger:Logger,strategy_registry:StrategyRegistry):
        self._TradingService: TradingService = trading_service
        self._NewsService = news_service
        self._TradeManager = trade_manager
        self._AssetManager = asset_manager
        self._Relation_manager = relation_manager
        self._StrategyRegistry = strategy_registry
        self._BacktestService = backtest_service
        self._logger = logger
    # endregion

    def run_backtest(self,json_data:Dict[str,Any] = None):
        try:
            self._BacktestService.start_backtesting_strategy(BacktestInput.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Backtest failed,Error: {e}".format(e=e))

    def get_asset_selection(self)->list[str]:
        return self._BacktestService.get_asset_selection()

    def get_test_results(self,strategy:str = None)->list[dict]:
        strategy_name = None

        results = self._BacktestService.get_test_results(strategy_name)
        updated_results = []
        for result in results:
            try:
                trade_str:dict = result.dict()
                updated_results.append(trade_str)
            except Exception as e:
                self._logger.error("Error appending trade to list: {id},Error:{e}".format(id=result.result_id,e=e))
                continue
        return updated_results

    def get_trades(self)->list[dict]:
        trades = self._TradeManager.return_storage_trades()
        updated_trades = []
        for trade in trades:
            try:
                trade_str:dict = trade.dict()
                updated_trades.append(trade_str)
            except Exception as e:
                self._logger.error("Error appending trade to list: {id},Error:{e}".format(id=trade.id,e=e))
                continue
        return updated_trades

    def get_news(self):
        news_days:list [NewsDay]= self._NewsService.return_news_days()
        updated_news = []
        for news_day in news_days:
            try:
                trade_str:dict = news_day.dict()
                updated_news.append(trade_str)
            except Exception as e:
                self._logger.error("Error appending trade to list: {id},Error:{e}".format(id=news_day,e=e))
                continue
        return updated_news

    def get_smt_pairs(self)->list[dict]:
        smt_pairs:list[SMTPair] = self._Relation_manager.return_smt_pairs()
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
            self._Relation_manager.create_smt(smt_pair)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def delete_smt_pair(self,json_data:Dict[str,Any] = None):
        try:
            smt_pair = SMTPair.model_validate(json_data)
            self._Relation_manager.delete_smt_pair(smt_pair)
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

    def add_relation(self,json_data:Dict[str,Any] = None):
        try:
            relation = Relation.model_validate(json_data)
            self._Relation_manager.create_relation(relation=relation)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))

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

    def get_assets(self)->list[dict]:
        assets = self._AssetManager.return_stored_assets()
        dict_assets = []
        for asset in assets:
            try:
                asset_dict:dict = asset.dict(exclude={'candles_series'})
                dict_assets.append(asset_dict)
            except Exception as e:
                self._logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=asset.__name, e=e))
                continue
        return dict_assets

    def add_asset(self, json_data: Dict[str, Any]) -> None:
        try:
            self._AssetManager.create_asset(Asset.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Add Asset failed,Error: {e}".format(e=e))

    def update_asset(self, json_data: Dict[str, Any]):
        try:
            self._AssetManager.update_asset(Asset.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Update Asset failed,Error: {e}".format(e=e))

    def delete_asset(self,json_data:Dict[str,Any] = None):
        try:
            asset = Asset.model_validate(json_data)
            self._AssetManager.delete_asset(asset)
        except Exception as e:
            self._logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def get_strategies(self):
        strategies:list[str] = self._Relation_manager.return_strategies()
        return strategies

    def get_brokers(self):
        brokers:list[BrokerDTO] = self._TradeManager.get_brokers()
        dict_brokers = []
        for broker in brokers:
            try:
                broker_dict:dict = broker.dict(exclude={"id"})
                dict_brokers.append(broker_dict)
            except Exception as e:
                self._logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=broker.__name, e=e))
                continue
        return dict_brokers

    def get_categories(self):
        categories:list[CategoryDTO] = self._Relation_manager.return_categories()
        dict_categories = []
        for category in categories:
            try:
                category_dict:dict = category.dict(exclude={"id"})
                dict_categories.append(category_dict)
            except Exception as e:
                self._logger.error("Error while dumping category name: {name},Error:{e}".format(name=category.__name, e=e))
                continue
        return dict_categories

    def get_asset_classes(self):
        asset_classes:list[AssetClassDTO] = self._AssetManager.return_asset_classes()
        dict_asset_classes = []
        for asset_class in asset_classes:
            try:
                asset_class_dict:dict = asset_class.dict(exclude={"id"})
                dict_asset_classes.append(asset_class_dict)
            except Exception as e:
                self._logger.error("Error while dumping Asset Class,Error:{e}".format(e=e))
                continue
        return dict_asset_classes

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
