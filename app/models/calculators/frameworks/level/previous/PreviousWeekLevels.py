from app.interfaces.framework.ILevel import ILevel
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level
from app.monitoring.logging.logging_startup import logger


class PreviousWeekLevels(ILevel):
    """Previous Week Levels"""
    def return_levels(self, candles: list[Candle]) -> list[Level]:
        try:
            logger.info("Previous Week Levels returning")
            weekly_levels = {}

            for candle in candles:
                # Extract the ISO year and week number
                year, week = candle.iso_time.isocalendar()[:2]
                week_key = (year, week)

                # Initialize or update the high and low for this week
                if week_key not in weekly_levels:
                    # Create Level objects for high and low
                    weekly_levels[week_key] = {
                        "high": Level(name="PWH", level=candle.high),
                        "low": Level(name="PWL", level=candle.low),
                    }
                else:
                    # Update high and low Level objects
                    if candle.high > weekly_levels[week_key]["high"].level:
                        weekly_levels[week_key]["high"].level = candle.high
                    if candle.low < weekly_levels[week_key]["low"].level:
                        weekly_levels[week_key]["low"].level = candle.low

                # Add the current candle to both high and low Level objects for this week
                weekly_levels[week_key]["high"].candles.append(candle)
                weekly_levels[week_key]["low"].candles.append(candle)

            # Flatten the dictionary into a list of Level objects
            result = [level for levels in weekly_levels.values() for level in levels.values()]
            return result
        except Exception as e:
            logger.error("Previous Week Levels failed with exception: {}".format(e))
