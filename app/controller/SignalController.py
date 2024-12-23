from typing import Dict, Any

from app.Services.TradingService import TradingService


class SignalController:

    # region Initializing
    def __init__(self, tradingService: TradingService):
        self._TradingService: TradingService = tradingService
    # endregion

    # region TradingView Handling
    def tradingViewSignal(self, jsonData: Dict[str, Any]) -> None:
        self._TradingService.handlePriceActionSignal(jsonData)
    # endregion
