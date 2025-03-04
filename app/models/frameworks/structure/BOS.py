from app.models.frameworks.structure.StructureEnum import StructureEnum
from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure
from app.monitoring.logging.logging_startup import logger


class BOS:

    def __init__(self):
        self.name = StructureEnum.BREAKOFSTRUCTURE.value

    def return_confirmation(self, candles: list[Candle]) -> list[Structure]:
        """
        Identify Break of Structure (BOS) from provided data.
        param data_points: A list of dictionaries with 'open', 'high', 'low', 'close' prices.
        :return: 'BOS_Bullish', 'BOS_Bearish' or None.
        """
        structures = []
        try:
            last_candle:Candle = candles[-1]
            highs = []
            lows = []
            closes = []

            for candle in candles:
                highs.append(candle.high)
                lows.append(candle.low)
                closes.append(candle.close)

            for i in range(len(candles)):
                # Track the last significant bullish high
                if i >= lookback:
                    if closes[i] > max(highs[i - lookback:i]):
                        structure = Structure(name=self.name, direction="Bullish", candles=[candles[i-1]]
                                              ,timeframe=last_candle.timeframe)
                        structures.append(structure)

                # Track the last significant bearish low
                if i >= lookback:
                    if closes[i] < min(lows[i - lookback:i]):
                        structure = Structure(name=self.name, direction="Bearish",candles=candles[i-1]
                                              ,timeframe=last_candle.timeframe)
                        structures.append(structure)
            return structures
        except Exception as e:
            logger.error("BOS Confirmation Exception: {}".format(e))
