from typing import Dict, Any

from app.db.mongodb.dtos.BrokerDTO import BrokerDTO
from app.helper.manager.AssetManager import AssetManager
from app.helper.manager.RelationManager import RelationManager
from app.helper.manager.StrategyManager import StrategyManager
from app.helper.manager.TradeManager import TradeManager
from app.models.asset.Asset import Asset
from app.models.asset.Relation import Relation
from app.models.asset.SMTPair import SMTPair
from app.models.backtest.BacktestInput import BacktestInput
from app.monitoring.logging.logging_startup import logger
from app.services.BacktestService import BacktestService
from app.services.NewsService import NewsService
from app.services.TradingService import TradingService
from tools.EconomicScrapper.Models.NewsDay import NewsDay


class SignalController:

    # region Initializing
    def __init__(self,trading_service:TradingService, news_service:NewsService,asset_manager:AssetManager, trade_manager:TradeManager
                 ,relation_manager:RelationManager,backtest_service:BacktestService):
        self._TradingService: TradingService = trading_service
        self._NewsService = news_service
        self._TradeManager = trade_manager
        self._AssetManager = asset_manager
        self._Relation_manager = relation_manager
        self._StrategyManager = StrategyManager()
        self._BacktestService = backtest_service
    # endregion

    def run_backtest(self,json_data:Dict[str,Any] = None):
        try:
            self._BacktestService.start_backtesting_strategy(BacktestInput.model_validate(json_data))
        except Exception as e:
            logger.warning("Backtest failed,Error: {e}".format(e=e))

    def get_asset_selection(self)->list[str]:
        return self._BacktestService.get_asset_selection()

    def get_test_results(self,strategy:str = None)->list[dict]:
        strategy_name = None
        try:
            strategy_name = strategy
            self._BacktestService.get_test_results(strategy_name)
        except Exception as e:
            logger.exception("Get Backtest Results,Exception: {e}".format(e=e))

        results = self._BacktestService.get_test_results(strategy_name)
        updated_results = []
        for result in results:
            try:
                trade_str:dict = result.dict()
                updated_results.append(trade_str)
            except Exception as e:
                logger.error("Error appending trade to list: {id},Error:{e}".format(id=result.result_id,e=e))
        return updated_results

    def get_trades(self)->list[dict]:
        trades = self._TradeManager.return_storage_trades()
        updated_trades = []
        for trade in trades:
            try:
                trade_str:dict = trade.dict()
                updated_trades.append(trade_str)
            except Exception as e:
                logger.error("Error appending trade to list: {id},Error:{e}".format(id=trade.id,e=e))
        return updated_trades

    def get_news(self):
        news_days:list [NewsDay]= self._NewsService.return_news_days()
        updated_news = []
        for news_day in news_days:
            try:
                trade_str:dict = news_day.dict()
                updated_news.append(trade_str)
            except Exception as e:
                logger.error("Error appending trade to list: {id},Error:{e}".format(id=news_day,e=e))
        return updated_news

    def update_trade(self):
        # todo close trade amend trade
        pass


    def add_trade(self):
        pass

    def delete_trade(self):
        pass

    def get_smt_pairs(self)->list[dict]:
        smt_pairs:list[SMTPair] = self._Relation_manager.return_smt_pairs()
        dict_smt_pairs = []
        for smt_pair in smt_pairs:
            try:
                relation_dict:dict = smt_pair.dict()
                dict_smt_pairs.append(relation_dict)
            except Exception as e:
                logger.error("Error appending relation to list: {id},Error:{e}".format(id=smt_pair.strategy,e=e))
        return dict_smt_pairs

    def add_smt_pair(self,json_data:Dict[str,Any] = None):
        try:
            smt_pair = SMTPair.model_validate(json_data)
            self._Relation_manager.create_smt(smt_pair)
        except Exception as e:
            logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def delete_smt_pair(self,json_data:Dict[str,Any] = None):
        try:
            smt_pair = SMTPair.model_validate(json_data)
            self._Relation_manager.delete_smt_pair(smt_pair)
        except Exception as e:
            logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def get_relations(self)->list[dict]:
        relations:list[Relation] = self._Relation_manager.return_relations()
        dict_relations = []
        for relation in relations:
            try:
                relation_dict:dict = relation.dict()
                dict_relations.append(relation_dict)
            except Exception as e:
                logger.error("Error appending relation to list: {id},Error:{e}".format(id=relation.id,e=e))
        return dict_relations

    def add_relation(self,json_data:Dict[str,Any] = None):
        try:
            relation = Relation.model_validate(json_data)
            self._Relation_manager.create_relation(relation=relation)
        except Exception as e:
            logger.warning("Delete Asset failed,Error: {e}".format(e=e))

    def update_relation(self,json_data:Dict[str,Any] = None):
        try:
            self._Relation_manager.update_relation(Relation.model_validate(json_data))
        except Exception as e:
            logger.warning("Update Relation failed,Error: {e}".format(e=e))

    def delete_relation(self,json_data:Dict[str,Any] = None):
        try:
            self._Relation_manager.delete_relation(Relation.model_validate(json_data))
        except Exception as e:
            logger.warning("Delete Relation failed,Error: {e}".format(e=e))

    def get_assets(self)->list[dict]:
        assets = self._AssetManager.return_stored_assets()
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
            logger.warning("Add Asset failed,Error: {e}".format(e=e))

    def update_asset(self, json_data: Dict[str, Any]):
        try:
            self._AssetManager.update_asset(Asset.model_validate(json_data))
        except Exception as e:
            logger.warning("Update Asset failed,Error: {e}".format(e=e))

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
