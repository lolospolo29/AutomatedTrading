from app.interfaces.framework.IConfirmation import IConfirmation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Structure import Structure
from app.monitoring.logging.logging_startup import logger


class BOS(IConfirmation):

    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "BOS"

    def return_confirmation(self, candles: list[Candle]) -> list[Structure]:
        """
        Identify Break of Structure (BOS) from provided data.
        param data_points: A list of dictionaries with 'open', 'high', 'low', 'close' prices.
        :return: 'BOS_Bullish', 'BOS_Bearish' or None.
        """
        structures = []
        try:
            if len(candles) < self.lookback:
                return []
            highs = []
            lows = []
            closes = []

            for candle in candles:
                highs.append(candle.high)
                lows.append(candle.low)
                closes.append(candle.close)


            for i in range(len(candles)):
                # Track the last significant bullish high
                if i >= self.lookback:
                    if closes[i] > max(highs[i - self.lookback:i]):
                        structure = Structure(name=self.name, direction="Bullish", candle=candles[i-1])
                        structures.append(structure)

                # Track the last significant bearish low
                if i >= self.lookback:
                    if closes[i] < min(lows[i - self.lookback:i]):
                        structure = Structure(name=self.name, direction="Bearish",candle=candles[i-1])
                        structures.append(structure)
            return structures
        except Exception as e:
            logger.error("BOS Confirmation Exception: {}".format(e))
