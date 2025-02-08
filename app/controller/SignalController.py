from typing import Dict, Any

from app.monitoring.logging.logging_startup import logger
from app.helper.facade.TradingFacade import TradingFacade
from app.services.TradingService import TradingService


class SignalController:

    # region Initializing
    def __init__(self):
        self._TradingService: TradingService = TradingService()
        self._TradingFacade: TradingFacade = TradingFacade()
    # endregion

    def get_news_days(self)->list[dict]:
        news_days = self._TradingFacade.get_news_days()
        updated_news_days = []
        for news_day in news_days:
            try:
                news_day_str:dict = news_day.to_dict()
                updated_news_days.append(news_day_str)
            except Exception as e:
                logger.error("Error appending news day to list: {id},Error:{e}".format(id=news_day.day_iso,e=e))
        return updated_news_days

    def get_trades(self)->list[dict]:
        trades = self._TradingFacade.get_trades()
        updated_trades = []
        for trade in trades:
            try:
                trade_str:dict = trade.to_dict()
                updated_trades.append(trade_str)
            except Exception as e:
                logger.error("Error appending trade to list: {id},Error:{e}".format(id=trade.id,e=e))
        return updated_trades

    def edit_trade(self):
        pass

    def add_trade(self):
        pass

    def delete_trade(self):
        pass

    def add_asset(self):
        pass

    def get_assets(self)->list[dict]:
        assets = self._TradingFacade.get_assets()
        updated_assets = []
        for asset in assets:
            try:
                asset_str:dict = asset.to_dict()
                updated_assets.append(asset_str)
            except Exception as e:
                logger.error("Error appending asset to list Name: {name},Error:{e}".format(name=asset.name,e=e))
        return updated_assets

    def delete_asset(self):
        pass

    def get_strategies(self):
        pass

    def add_strategy(self):
        pass

    def delete_strategy(self):
        pass

    # region TradingView Handling
    def trading_view_signal(self, json_data: Dict[str, Any]) -> None:
        try:
            self._TradingService.handle_price_action_signal(json_data)
        except Exception as e:
            logger.warning("Price Action Signal failed,Error: {e}".format(e=e))
    # endregion
