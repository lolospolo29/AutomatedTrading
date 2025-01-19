from typing import Dict, Any

from app.monitoring.logging.logging_startup import logger
from app.services.TradingService import TradingService


class SignalController:

    # region Initializing
    def __init__(self):
        self._TradingService: TradingService = TradingService()
    # endregion

    # region TradingView Handling
    def trading_view_signal(self, json_data: Dict[str, Any]) -> None:
        try:

            self._TradingService.handle_price_action_signal(json_data)
        except Exception as e:
            logger.error(e)
    # endregion
