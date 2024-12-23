from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level


class equalHL:  ### Implement threshold for every asset every Timeframe
    def __init__(self, threshold_index=2, threshold_stocks=2, mintick=0.0001):
        """Initialize with a tolerance to consider lows/highs as equal and thresholds."""
        self.threshold_index: float = threshold_index
        self.threshold_stocks: float = threshold_stocks
        self.mintick: float = mintick

        # Determine the threshold for equalness
        # if self.mintick >= 0.1:
        #     self.threshold: float = self.threshold_index * self.mintick
        # else:
        #     self.threshold: float = self.threshold_stocks * self.mintick
        self.threshold = 150

    def returnLevels(self, candles: list[Candle], detect: str) -> list[Level]:
        equalLevels = []
        equalLows = []
        equalHighs = []

        lastcandle = candles[-1]
        timeframe = lastcandle.timeFrame

        # Detect equal lows
        if detect == "low" or detect == "both":
            filteredCandles = self.filterCandles(candles,"low")
            equalLows += self._detect_equal_lows(filteredCandles,timeframe)

        # Detect equal highs
        if detect == "high" or detect == "both":
            filteredCandles = self.filterCandles(candles,"high")
            equalHighs += self._detect_equal_highs(filteredCandles,timeframe)

        # Filter equal levels to only keep the lowest or highest in the same threshold range
        equalLevels += self._filter_levels(equalLows)
        equalLevels += self._filter_levels(equalHighs)

        return equalLevels

    @staticmethod
    def filterCandles(candles: list[Candle], detect: str) -> list[Candle]:
        filteredCandles = []
        if detect == "low":
            for candle in candles:
                if candle.open < candle.close:
                    filteredCandles.append(candle)
        if detect == "high":
            for candle in candles:
                if candle.open > candle.close:
                    filteredCandles.append(candle)
        return filteredCandles


    def _detect_equal_lows(self, candles: list[Candle], timeframe) -> list[Level]:
        equalLows = []
        lows = []
        ids = []

        # Collecting high and low values from each data point
        for candle in candles:
            lows.append(candle.low)
            ids.append(candle.id)

        # Check for equal lows
        for i in range(len(lows)):
            currentLow = lows[i]
            similarLows = []
            similarIds = []

            # Compare with the remaining lows
            for j in range(i + 1, len(lows)):
                if abs(lows[j] - currentLow) < self.threshold:
                    # Check if any price has gone lower after this potential equal low
                    if not any(low < currentLow for low in lows[j:]) and lows[j] != currentLow:
                        similarLows.append((lows[j]))  # Add the similar low
                        similarIds.append(ids[j])


            # If we found similar lows, add them as levels
            if similarLows:
                if len(equalLows) >= 1:
                    for k in range(len(similarLows)):
                        isInLows = False
                        for equalLow in equalLows:
                            if equalLow.level == similarLows[k]:
                                isInLows = True
                        if not isInLows:
                            level = Level(name="EqualLow", level=similarLows[k])
                            level.timeFrame = timeframe
                            level.setFibLevel(0.0, "EQL", [similarIds[k]])
                            equalLows.append(level)
                if len(equalLows) <= 0:
                    for k in range(len(similarLows)):
                        level = Level(name="EqualLow", level=similarLows[k])
                        level.timeFrame = timeframe
                        level.setFibLevel(0.0, "EQL", [similarIds[k]])
                        equalLows.append(level)

        return equalLows

    def _detect_equal_highs(self, candles: list[Candle], timeFrame) -> list[Level]:
        equalHighs = []
        highs = []
        ids = []

        # Collecting high and low values from each data point
        for candle in candles:
            highs.append(candle.high)
            ids.append(candle.id)

        # Check for equal highs
        for i in range(len(highs)):
            currentHigh = highs[i]
            similarHighs = []
            similarIds = []

            # Compare with the remaining highs
            for j in range(i + 1, len(highs)):
                if abs(highs[j] - currentHigh) < self.threshold:
                    # Check if any price has gone higher after this potential equal high
                    if not any(high > currentHigh for high in highs[j:]) and highs[j] != currentHigh:
                        similarHighs.append((highs[j]))  # Add the similar high
                        similarIds.append(ids[j])

            # If we found similar highs, add them as levels
            if similarHighs:
                if len(equalHighs) >= 1:
                        for k in range(len(similarHighs)):
                            isInEqualHighs = False
                            for equalHigh in equalHighs:
                                if equalHigh.level == similarHighs[k]:
                                    isInEqualHighs = True
                            if not isInEqualHighs:
                                level = Level(name="EqualHigh", level=similarHighs[k])
                                level.timeFrame = timeFrame
                                level.setFibLevel(0.0, "EQH", [similarIds[k]])
                                equalHighs.append(level)
                if len(equalHighs) <= 0:
                    for k in range(len(similarHighs)):
                        level = Level(name="EqualHigh", level=similarHighs[k])
                        level.timeFrame = timeFrame
                        level.setFibLevel(0.0, "EQH", [similarIds[k]])
                        equalHighs.append(level)

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
            if abs(levels[i].level - currentGroup[-1].level) < self.threshold:
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
