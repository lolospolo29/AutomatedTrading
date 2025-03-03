from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger

class Fibonnaci:
    def __init__(self,levels:list[float],name:str):

        # Fibonacci retracement levels to calculate
        self.retracement_levels: list[float] = levels
        self.name = name

    def return_levels(self, high:float,low:float) -> list[Level]:
        """
        Projects the High and the Low of the given Candles with Lookback
        :param high:
        :param low:
        """
        all_levels = []

        try:
            levels = self._generate_fib_levels_bullish(high,low)
            all_levels.extend(levels)
            levels = self._generate_fib_levels_bearish(high,low)
            all_levels.extend(levels)

        except Exception as e:
            logger.error("Return Levels failed with exception:{e}".format(e=e))
        finally:
            return all_levels

    def _generate_fib_levels_bullish(self,high:float,low:float) -> list[Level]:
        levels = []
        for fib_level in self.retracement_levels:
            bullish_level = high - fib_level * (high - low)
            levels.append(Level(name=self.name, level=bullish_level,fib_level=fib_level,
                                candles=[candles[-1],candles[0]],direction="Bullish",timeframe=last_candle.timeframe))
        return levels

    def _generate_fib_levels_bearish(self,high:float,low:float) -> list[Level]:
        levels = []
        last_candle:Candle = candles[-1]
        for fib_level in self.retracement_levels:
            bearish_level = low + fib_level  * (high - low)
            levels.append(Level(name=self.name, level=bearish_level,fib_level=fib_level,
                                candles=[candles[-1],candles[0]],direction="Bearish",timeframe=last_candle.timeframe))
        return levels