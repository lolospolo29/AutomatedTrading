from files.interfaces.ITimeWindow import ITimeWindow
from files.models.asset.Candle import Candle
from files.models.frameworks.Level import Level


class PreviousSessionLevels:
    """Calculator for Previous Session Levels"""

    @staticmethod
    def return_levels(candles: list[Candle], window:ITimeWindow) -> list[Level]:
        """
        Calculate the high and low of candles within each session defined by time windows.

        Args:
            candles (List[Candle]): List of Candle objects.
            time_windows (List[ITimeWindow]): List of ITimeWindow implementations.

        Returns:
            List[Level]: List of Level objects with names matching the session name.
            :param candles:
            :param window:
        """
        session_levels = []

        try:
            last_candle: Candle = candles[-1]

            session_name = window.__class__.__name__  # Use class name as session identifier

            high_level = Level(name=f"{session_name} High", level=float('-inf'), direction="Bearish", fib_level=0.0
                               , candles=[], timeframe=last_candle.timeframe)

            low_level = Level(name=f"{session_name} Low", level=float('inf'), direction="Bullish", fib_level=0.0
                              , candles=[], timeframe=last_candle.timeframe)

            for candle in candles:
                if window.is_in_entry_window(candle.iso_time):
                    # Update high and low levels
                    if candle.high > high_level.level:
                        high_level.level = candle.high
                        high_level.candles.append(candle)
                    if candle.low < low_level.level:
                        low_level.level = candle.low
                        low_level.candles.append(candle)

            # Add the high and low levels to the list
            session_levels.append(high_level)
            session_levels.append(low_level)

            return session_levels
        except Exception as e:
            pass
        finally:
            return session_levels