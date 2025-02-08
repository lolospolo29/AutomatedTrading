from datetime import datetime

from app.models.strategy.SMTStrategy import SMTStrategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class TestSMTStrategy(SMTStrategy):


    def __init__(self,asset_1:str,asset_2:str,correlation:str):
        """
        Initializes the TestSMTStrategy for testing SMT functionality.

        """
        timeFrames = []
        name = "TestSMTStrategy"
        super().__init__(name, timeFrames,asset_1,asset_2,correlation)

    def get_exit(self, candles: list, timeFrame: int, trade: Trade) -> StrategyResult:
        """
        Mock implementation of the exit strategy. For testing purposes, it exits
        when there are more than 10 candles.

        Parameters:
            candles (list): List of candles.
            timeFrame (int): The applicable timeframe.
            trade (Trade): The current trade being analyzed.

        Returns:
            StrategyResult: Dummy result indicating exit conditions met.
        """
        return StrategyResult(Trade())

    def get_entry(self, candles: list, timeFrame: int) -> StrategyResult:
        """
        Mock implementation of the entry strategy. For testing purposes, it enters
        if the candle list contains exactly 5 candles.

        Parameters:
            candles (list): List of candles.
            timeFrame (int): The applicable timeframe.

        Returns:
            StrategyResult: Dummy result indicating entry conditions met.
        """
        return StrategyResult(Trade())

    def is_in_time(self, time) -> bool:
        """
        Mock implementation to always indicate the trade is within the allowed time.

        Parameters:
            time (datetime): The time to check.

        Returns:
            bool: Always True for testing.
        """
        return True
