from app.interfaces.framework.IConfirmation import IConfirmation
from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure
from app.monitoring.logging.logging_startup import logger


class Choch(IConfirmation):

    def __init__(self, lookback: int):
        self.lookback: int = lookback
        self.name = "CHOCH"

    @staticmethod
    def is_bullish_fractal(highs: list, index: int, lookback: int) -> bool:
        """Check if there is a bullish fractal at the given index (local high)"""
        p = lookback // 2
        if index < p or index >= len(highs) - p:
            return False
        # Check if it's a local maximum
        for i in range(1, p + 1):
            if highs[index] <= highs[index - i] or highs[index] <= highs[index + i]:
                return False
        return True

    @staticmethod
    def is_bearish_fractal(lows: list, index: int, lookback: int) -> bool:
        """Check if there is a bearish fractal at the given index (local low)"""
        p = lookback // 2
        if index < p or index >= len(lows) - p:
            return False
        # Check if it's a local minimum
        for i in range(1, p + 1):
            if lows[index] >= lows[index - i] or lows[index] >= lows[index + i]:
                return False
        return True

    def return_confirmation(self, candles: list[Candle]) -> list[Structure]:
        """
        Identify Change of Character (ChoCH) from provided data.
        _param data_points: A list of dictionaries with 'open', 'high', 'low', 'close' prices.
        :return: 'Choch_Bullish', 'Choch_Bearish' or None.
        """
        structures = []
        try:
            if len(candles) < self.lookback:
                return []
            highs = []
            lows = []
            closes = []
            ids = []

            for candle in candles:
                highs.append(candle.high)
                lows.append(candle.low)
                closes.append(candle.close)
                ids.append(candle.id)

            upper_fractal = None
            lower_fractal = None

            for i in range(self.lookback // 2, len(candles) - self.lookback // 2):
                # Check for bullish fractal
                if self.is_bullish_fractal(highs, i, self.lookback):
                    upper_fractal = {'value': highs[i], 'index': i, 'crossed': False}

                # Check for bearish fractal
                if self.is_bearish_fractal(lows, i, self.lookback):
                    lower_fractal = {'value': lows[i], 'index': i, 'crossed': False}

                # Check crossover above the bullish fractal (ChoCH/BOS Bullish)
                if upper_fractal and closes[i] > upper_fractal['value'] and not upper_fractal['crossed']:
                    upper_fractal['crossed'] = True

                    structure =  Structure(name=self.name, direction="Bullish", candle=candles[i])
                    structures.append(structure)

                # Check crossover below the bearish fractal (ChoCH/BOS Bearish)
                if lower_fractal and closes[i] < lower_fractal['value'] and not lower_fractal['crossed']:
                    lower_fractal['crossed'] = True
                    structure =  Structure(name=self.name, direction="Bearish", candle=candles[i])
                    structures.append(structure)
        except Exception as e:
            logger.error("CHOCH Confirmation Exception: {}".format(e))
        return structures
