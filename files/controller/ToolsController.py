from logging import Logger
from typing import Dict, Any

from files.models.backtest.BacktestInput import BacktestInput
from files.services.BacktestService import BacktestService
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.NewsService import NewsService


class ToolsController:

    # region Initializing
    def __init__(self,news_service:NewsService,
                  backtest_service:BacktestService, logger:Logger):
        self._NewsService = news_service
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
        results = self._BacktestService.get_test_results(strategy)
        updated_results = []
        for result in results:
            try:
                trade_str:dict = result.dict()
                updated_results.append(trade_str)
            except Exception as e:
                self._logger.error("Error appending trade to list: {id},Error:{e}".format(id=result.result_id,e=e))
                continue
        return updated_results

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