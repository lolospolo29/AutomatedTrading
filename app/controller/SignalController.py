from typing import Dict, Any

from app.services.TradingService import TradingService


class SignalController:

    # region Initializing
    def __init__(self):
        self._TradingService: TradingService = TradingService()
    # endregion

    # region TradingView Handling
    def trading_view_signal(self, json_data: Dict[str, Any]) -> None:
        self._TradingService.handle_price_action_signal(json_data)
    # endregion
