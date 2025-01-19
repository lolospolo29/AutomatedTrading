from app.interfaces.framework.ILevel import ILevel
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger


class PreviousDaysLevels(ILevel):
    """Previous Days Level Calculation using the Fibonnaci"""

    def return_levels(self, candles: list[Candle]) -> list[Level]:
        """
        Calculate the high and low of candles within each Day.

        Args:
            candles (List[Candle]): List of Candle objects.

        Returns:
            List[Level]
        """
        daily_levels = {}
        try:

            for candle in candles:
                # Extract the date from isoTime (ignore time part)
                day = candle.iso_time.date()

                # Initialize or update the high and low for this day
                if day not in daily_levels:
                    # Create Level objects for high and low
                    daily_levels[day] = {
                        "high": Level(name="PDH", level=candle.high),
                        "low": Level(name="PDL", level=candle.low),
                    }
                else:
                    # Update high and low Level objects
                    if candle.high > daily_levels[day]["high"].level:
                        daily_levels[day]["high"].level = candle.high
                    if candle.low < daily_levels[day]["low"].level:
                        daily_levels[day]["low"].level = candle.low

                # Add the current candle to both high and low Level objects for this day
                daily_levels[day]["high"].candles.append(candle)
                daily_levels[day]["low"].candles.append(candle)

            # Flatten the dictionary into a list of Level objects
            result = [level for levels in daily_levels.values() for level in levels.values()]
            return result
        except Exception as e:
            logger.error("Previous Days Levels Error" + str(e))
