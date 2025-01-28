from app.helper.handler.SMTHandler import SMTHandler
from app.models.strategy.Strategy import Strategy
from app.models.trade.Trade import Trade
from app.models.strategy.StrategyResult import StrategyResult
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame


class SMTStrategy(Strategy):
    def __init__(self, name: str, timeFrames: list[ExpectedTimeFrame],asset_1:str,asset_2:str,correlation:str):
        """
        Initializes the SMTStrategy object.

        Parameters:
            name (str): The name of the strategy.
            timeFrames (list[ExpectedTimeFrame]): Timeframes applicable for the strategy.
        """
        super().__init__(name, timeFrames)
        # Set assets and correlation
        self.asset_1 = asset_1
        self.asset_2 = asset_2
        self.correlation = correlation
        self._smt_handler = SMTHandler(asset_1=self.asset_1,
                                       asset_2=self.asset_2,
                                       correlation=self.correlation)

    def get_exit(self, candles: list, timeFrame: int, trade: Trade) -> StrategyResult:
        """
        Placeholder method for calculating the exit strategy.
        """
        raise NotImplementedError("SMTStrategy.get_exit must be implemented.")

    def get_entry(self, candles: list, timeFrame: int) -> StrategyResult:
        """
        Placeholder method for calculating the entry strategy.
        """
        raise NotImplementedError("SMTStrategy.get_entry must be implemented.")

    def is_in_time(self, time) -> bool:
        """
        Placeholder method for determining whether a trade opportunity exists during the specified time.
        """
        raise NotImplementedError("SMTStrategy.is_in_time must be implemented.")
