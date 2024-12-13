from typing import Dict, Any


class SignalController:
    def __init__(self, TradingController):
        self._TradingController = TradingController

    def tradingViewSignal(self, jsonData: Dict[str, Any]) -> None:
        self._TradingController.handlePriceActionSignal(jsonData)
