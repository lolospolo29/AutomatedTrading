from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.exceptions.CalculationExceptionError import CalculationExceptionError
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class FVG(IPDArray):
    """
    FVG Calculation,which Consist of the Candles trading in the same Direction.
    Leaving a Gap between the first and third"""

    def __init__(self):
        self.name = "FVG"

    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        try:
            low,high =self.return_candle_range(pd_array)
            if order_direction.BUY:
                if risk_mode.SAFE:
                    return low
                if risk_mode.AGGRESSIVE:
                    return high

            if order_direction.SELL:
                if risk_mode.SAFE:
                    return high
                if risk_mode.AGGRESSIVE:
                    return low

            if risk_mode.MODERAT:
                low = low
                high = high
                return (low + high) / 2
        except Exception as e:
            logger.error("FVG Entry Error with Exception"+str(e))


    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        try:
            highs = [candle.high for candle in pd_array.candles]
            lows = [candle.low for candle in pd_array.candles]
            close =  [candle.close for candle in pd_array.candles]
            open = [candle.open for candle in pd_array.candles]

            if order_direction.BUY:
                if risk_mode.SAFE:
                    return min(lows)
                if risk_mode.MODERAT:
                    return min(open)
                if risk_mode.AGGRESSIVE:
                    return min(close)
            if order_direction.SELL:
                if risk_mode.SAFE:
                    return max(highs)
                if risk_mode.MODERAT:
                    return max(open)
                if risk_mode.AGGRESSIVE:
                    return max(close)
        except Exception as e:
            logger.error("FVG Stop Error with Exception"+str(e))

    def checkForInverse(self, pd_array: PDArray, candles: list[Candle]) ->str:
        """
        Sets the Status of the PDArray to Inverse if it is traded through,resets if inverse another time.
        :param pd_array:
        :param candles:
        :return:
        """
        try:

            # Extract the two IDs from the PDArray
            _ids = [candle.id for candle in pd_array.candles]

            # Find the indices of these two IDs in the list of candles
            index1 = next((i for i, c in enumerate(candles) if c.id == _ids[0]), None)
            index2 = next((i for i, c in enumerate(candles) if c.id == _ids[1]), None)
            index3 = next((i for i, c in enumerate(candles) if c.id == _ids[2]), None)

            if index1 is None or index2 is None:
                raise ValueError("One or both IDs from PDArray not found in the candle list.")

            # Determine the older index (the one with the higher value)
            older_index = min(index1, index2,index3)

            start_index = older_index + 1

            # Extract and return the candles
            neighbors = candles[start_index:]

            if len(neighbors) > 0:
                for candle in neighbors:
                    low,high = self.return_candle_range(pd_array)
                    if pd_array.direction == "Bullish":
                        if candle.close < low:
                            return "Bearish"
                    if pd_array.direction == "Bearish":
                        if candle.close > high:
                            return "Bullish"
            return pd_array.direction
        except Exception as e:
            logger.error("FVG Inverse Error with Exception"+str(e))

    def return_candle_range(self, pd_array: PDArray) -> tuple[float,float]:
        """
        Returns the gap in the FVG.

        :param pd_array: A PDArray object that contains the IDs of the six candles forming the FVG.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """
        try:
            # Extract prices from the candles
            highs = [candle.high for candle in pd_array.candles]
            lows = [candle.low for candle in pd_array.candles]

            low = min(highs)
            high = max(lows)

            # Return the gap range
            return low, high
        except Exception as e:
            logger.error("FVG return candle range error with Exception"+str(e))

    def return_array_list(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        """
        Calculates a FVG by taking 3 consecutive Candles leaving a Gap between the first and third.
        :param lookback:
        :param candles:
        :return:
        """
        pd_arrays = []
        try:
            # Step 1: Apply lookback to limit the range of candles
            if lookback is not None and len(candles) > lookback:
                candles = candles[-lookback:]  # Slice the list to the last `lookback` elements
            if lookback is not None and len(candles) < lookback:
                return []

            opens = [candle.open for candle in candles]
            highs = [candle.high for candle in candles]
            lows = [candle.low for candle in candles]
            close = [candle.close for candle in candles]

            n = len(opens)
            if n > 2:
                # Loop through the data and check 3 consecutive candles for FVGs
                for i in range(2, n):  # Start bei der 3. Kerze (Index 2)
                    open1, high1, low1, close1 = opens[i - 2], highs[i - 2], lows[i - 2], close[i - 2]
                    open2, high2, low2, close2 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1]
                    open3, high3, low3, close3 = opens[i], highs[i], lows[i], close[i]

                    # Überprüfung auf Bearish FVG
                    if low1 > high3 and close2 < low1:
                        pdArray = PDArray(name=self.name, direction='Bearish')
                        pdArray.candles.append(candles[i])
                        pdArray.candles.append(candles[i - 1])
                        pdArray.candles.append(candles[i - 2])
                        pd_arrays.append(pdArray)

                    # Überprüfung auf Bullish FVG
                    elif high1 < low3 and close2 > high1:
                        pdArray = PDArray(name=self.name, direction='Bullish')
                        pdArray.candles.append(candles[i])
                        pdArray.candles.append(candles[i - 1])
                        pdArray.candles.append(candles[i - 2])
                        pd_arrays.append(pdArray)
        except Exception as e:
            logger.error("FVG Error with Exception"+str(e))
        finally:
            return pd_arrays

