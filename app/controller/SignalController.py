from typing import Dict, Any

from app.services.TradingService import TradingService


class SignalController:

    # region Initializing
    def __init__(self):
        self._TradingService: TradingService = TradingService()
    # endregion

    # region TradingView Handling
    def tradingViewSignal(self, jsonData: Dict[str, Any]) -> None:
        self._TradingService.handlePriceActionSignal(jsonData)
    # endregion
