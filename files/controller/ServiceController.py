from typing import Dict, Any

from logging import Logger

from files.models.backtest.BacktestInput import BacktestInput
from files.models.trade.Broker import Broker
from files.services.BacktestService import BacktestService
from files.services.BrokerService import BrokerService
from files.services.TradingService import TradingService
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.NewsService import NewsService


class ServiceController:

    # region Initializing
    def __init__(self, trading_service:TradingService, broker_service:BrokerService
                 , backtest_service:BacktestService,news_service:NewsService,logger:Logger):
        self._TradingService: TradingService = trading_service
        self._BrokerService = broker_service
        self._BacktestService = backtest_service
        self._NewsService = news_service
        self._logger = logger
    # endregion

    def get_trades(self)->list[dict]:
        trades = self._BrokerService.return_storage_trades()
        updated_trades = []
        for trade in trades:
            try:
                trade_str:dict = trade.dict(exclude={"_id"})
                updated_trades.append(trade_str)
            except Exception as e:
                self._logger.error("Error appending trade to list: {id},Error:{e}".format(id=trade.strategy_id, e=e))
                continue
        return updated_trades

    def get_brokers(self):
        brokers:list[Broker] = self._BrokerService.get_brokers()
        dict_brokers = []
        for broker in brokers:
            try:
                broker_dict:dict = broker.dict(exclude={"_id"})
                dict_brokers.append(broker_dict)
            except Exception as e:
                self._logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=broker._name, e=e))
                continue
        return dict_brokers

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

    def get_asset_selection(self)->list[str]:
        return self._BacktestService.get_asset_selection()

    def get_test_results(self,strategy:str = None)->list[dict]:
        results = self._BacktestService.get_test_results(strategy)
        updated_results = []
        for result in results:
            try:
                trade_str:dict = result.dict(exclude={"_id"})
                updated_results.append(trade_str)
            except Exception as e:
                self._logger.error("Error appending trade to list: {id},Error:{e}".format(id=result.result_id,e=e))
                continue
        return updated_results

    def run_backtest(self,json_data:Dict[str,Any] = None):
        try:
            self._BacktestService.start_backtesting_strategy(BacktestInput.model_validate(json_data))
        except Exception as e:
            self._logger.warning("Backtest failed,Error: {e}".format(e=e))

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
