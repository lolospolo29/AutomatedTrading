from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level


class equalHL:  ### Implement threshold for every asset every Timeframe
    def _findMedian(self,values:list[float]):
        sums = sum(values)
        return sums/len(values)


    def _calculateThreshold(self, prices:list[float]):
        prev_price = 0
        differences = []
        for price in prices:
            if prev_price == 0:
                prev_price = price
            if prev_price != price:
                differences.append(abs(price - prev_price))
                prev_price = price
        if differences:
            return self._findMedian(differences)


    def returnLevels(self, candles: list[Candle], detect: str) -> list[Level]:
        equal_levels = []
        equal_lows = []
        equal_highs = []

        last_candle = candles[-1]

        timeframe = last_candle.timeframe

        # Detect equal lows
        if detect == "low" or detect == "both":
            filteredCandles = self.filterCandles(candles,"low")
            equal_lows += self._detect_equal_lows(filteredCandles,timeframe)

        # Detect equal highs
        if detect == "high" or detect == "both":
            filteredCandles = self.filterCandles(candles,"high")
            equal_highs += self._detect_equal_highs(filteredCandles,timeframe)

        # Filter equal levels to only keep the lowest or highest in the same threshold range
        equal_levels += self._filter_levels(equal_lows)
        equal_levels += self._filter_levels(equal_highs)

        return equal_levels

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
        threshold = self._calculateThreshold(lows)
        # Check for equal lows
        for i in range(len(lows)):
            currentLow = lows[i]
            similarLows = []
            similarCandles = []

            # Compare with the remaining lows
            for j in range(i + 1, len(lows)):
                if abs(lows[j] - currentLow) < threshold:
                    # Check if any price has gone lower after this potential equal low
                    if not any(low < currentLow for low in lows[j:]) and lows[j] != currentLow:
                        similarLows.append((lows[j]))  # Add the similar low
                        similarCandles.append(candles[j])


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
                            level.set_fib_level(0.0, "EQL", candles=[similarCandles[k]])
                            equalLows.append(level)
                if len(equalLows) <= 0:
                    for k in range(len(similarLows)):
                        level = Level(name="EqualLow", level=similarLows[k])
                        level.timeFrame = timeframe
                        level.set_fib_level(0.0, "EQL", candles=[similarCandles[k]])
                        equalLows.append(level)

        return equalLows

    def _detect_equal_highs(self, candles: list[Candle], timeFrame) -> list[Level]:
        equalHighs = []
        highs = []

        # Collecting high and low values from each data point
        for candle in candles:
            highs.append(candle.high)
        treshold = self._calculateThreshold(highs)
        # Check for equal highs
        for i in range(len(highs)):
            currentHigh = highs[i]
            similarHighs = []
            similarCandles = []

            # Compare with the remaining highs
            for j in range(i + 1, len(highs)):
                if abs(highs[j] - currentHigh) < treshold:
                    # Check if any price has gone higher after this potential equal high
                    if not any(high > currentHigh for high in highs[j:]) and highs[j] != currentHigh:
                        similarHighs.append((highs[j]))  # Add the similar high
                        similarCandles.append(similarCandles[j])

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
                                level.set_fib_level(0.0, "EQH", candles=[similarCandles[k]])
                                equalHighs.append(level)
                if len(equalHighs) <= 0:
                    for k in range(len(similarHighs)):
                        level = Level(name="EqualHigh", level=similarHighs[k])
                        level.timeFrame = timeFrame
                        level.set_fib_level(0.0, "EQH", candles=[similarCandles[k]])
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
        levelsValue = [level.level in levels for level in levels]

        threshold = self._calculateThreshold(levelsValue)

        currentGroup = [levels[0]]  # Start with the first level

        for i in range(1, len(levels)):
            # If the current level is within the threshold range of the previous, group them together
            if abs(levels[i].level - currentGroup[-1].level) < threshold:
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
