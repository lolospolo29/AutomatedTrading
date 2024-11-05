from Interfaces.Strategy.ILevel import ILevel
from Models.Main.Asset import Candle
from Models.StrategyAnalyse.Level import Level


class equalHL(ILevel):  ### Implement threshold for every Asset every Timeframe
    def __init__(self, threshold_index=2, threshold_stocks=10, mintick=0.0001):
        """Initialize with a tolerance to consider lows/highs as equal and thresholds."""
        self.threshold_index: float = threshold_index
        self.threshold_stocks: float = threshold_stocks
        self.mintick: float = mintick

        # Determine the threshold for equalness
        if self.mintick >= 0.1:
            self.threshold: float = self.threshold_index * self.mintick
        else:
            self.threshold: float = self.threshold_stocks * self.mintick

    def getLevels(self, candles: list[Candle], detect: str) -> list[Level]:
        equalLevels = []

        # Detect equal lows
        if detect == "low" or detect == "both":
            equalLevels += self._detect_equal_lows(candles)

        # Detect equal highs
        if detect == "high" or detect == "both":
            equalLevels += self._detect_equal_highs(candles)

        # Filter equal levels to only keep the lowest or highest in the same threshold range
        equalLevels = self._filter_levels(equalLevels)

        return equalLevels

    def _detect_equal_lows(self, candles: list[Candle]) -> list[Level]:
        equalLows = []
        lows = candles.low  # Access the low prices
        timeStamp = candles.timeStamp  # Access timestamps for better tracking

        # Check for equal lows
        for i in range(len(lows)):
            currentLow = lows[i]
            similarLows = []

            # Compare with the remaining lows
            for j in range(i + 1, len(lows)):
                if abs(lows[j] - currentLow) <= self.threshold:
                    # Check if any price has gone lower after this potential equal low
                    if not any(low < currentLow for low in lows[j:]):
                        similarLows.append((lows[j], timeStamp[j]))  # Add the similar low and its timestamp

            # If we found similar lows, add them as levels
            if similarLows:
                equalLows.append(Level(name="EqualLow", level=currentLow))

        return equalLows

    def _detect_equal_highs(self, candles: list[Candle]) -> list[Level]:
        equalHighs = []
        highs = candles.high  # Access the high prices
        timeStamp = candles.timeStamp  # Access timestamps for better tracking

        # Check for equal highs
        for i in range(len(highs)):
            currentHigh = highs[i]
            similarHighs = []

            # Compare with the remaining highs
            for j in range(i + 1, len(highs)):
                if abs(highs[j] - currentHigh) <= self.threshold:
                    # Check if any price has gone higher after this potential equal high
                    if not any(high > currentHigh for high in highs[j:]):
                        similarHighs.append((highs[j], timeStamp[j]))  # Add the similar high and its timestamp

            # If we found similar highs, add them as levels
            if similarHighs:
                equalHighs.append(Level(name="EqualHigh", level=currentHigh))

        return equalHighs

    def _filter_levels(self, levels: list[Level]) -> list[Level]:
        """
        Filters the detected equal levels to retain only the most significant level
        (lowest for lows, highest for highs) within the same threshold range.
        """
        if not levels:
            return levels

        filteredLevels = []
        levels.sort(key=lambda x: x.level)  # Sort by price level

        currentGroup = [levels[0]]  # Start with the first level

        for i in range(1, len(levels)):
            # If the current level is within the threshold range of the previous, group them together
            if abs(levels[i].level - currentGroup[-1].level) <= self.threshold:
                currentGroup.append(levels[i])
            else:
                # If a new group starts, filter the current group and add to the result
                filteredLevels.append(self._get_significant_level(currentGroup))
                currentGroup = [levels[i]]

        # Handle the last group
        if currentGroup:
            filteredLevels.append(self._get_significant_level(currentGroup))

        return filteredLevels

    @staticmethod
    def _get_significant_level(levels: list[Level]) -> Level:
        """
        Returns the most significant level from a list of levels.
        For lows, this is the lowest level.
        For highs, this is the highest level.
        """
        # For equal lows, we take the lowest level
        if levels[0].name == "EqualLow":
            return min(levels, key=lambda x: x.level)
        # For equal highs, we take the highest level
        else:
            return max(levels, key=lambda x: x.level)
