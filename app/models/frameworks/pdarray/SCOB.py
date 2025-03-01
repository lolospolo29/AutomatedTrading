from app.models.frameworks.pdarray.PDEnum import PDEnum
from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.frameworks.PDArray import PDArray
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class Orderblock(IPDArray):
    def __init__(self):
        self.name: str = PDEnum.SCOB.value

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
                return (low + high) / 2
        except Exception as e:
            logger.error("Orderblock Entry Error with Exception"+str(e))


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
            logger.error("Orderblock Stop Error with Exception"+str(e))


    def checkForInverse(self, pd_array: PDArray, candles: list[Candle]) -> str:
        try:
            # Extract the two IDs from the PDArray
            _ids = [candle.id for candle in pd_array.candles]

            # Find the indices of these two IDs in the list of candles
            index1 = next((i for i, c in enumerate(candles) if c.id == _ids[0]), None)
            index2 = next((i for i, c in enumerate(candles) if c.id == _ids[1]), None)

            if index1 is None or index2 is None:
                raise ValueError("One or both IDs from PDArray not found in the candle list.")

            # Determine the older index (the one with the higher value)
            older_index = min(index1, index2)

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
            logger.error("Orderblock Inverse Error with Exception"+str(e))

    def return_candle_range(self, pdArray: PDArray) -> tuple[float, float]:
        """
        Returns the high and low of the OB.

        :param pdArray: A PDArray object that contains candles.
        :return: A dictionary containing the gap range {'low': ..., 'high': ...}.
        """
        try:
            # Extract prices from the candles
            highs = [candle.high for candle in pdArray.candles]
            lows = [candle.low for candle in pdArray.candles]

            high = max(highs)
            low = min(lows)

            return low,high
        except Exception as e:
            logger.error("Orderblock return candle range error with Exception"+str(e))

    def return_pd_arrays(self, candles: list[Candle], lookback: int = None) -> list[PDArray]:
        """Calculate the OB. By one Candle sweeps the other and finishes in the opposite direction."""
        # Step 1: Apply lookback to limit the range of candles
        pd_arrays = []

        try:
            last_candle:Candle = candles[-1]
            if lookback is not None and len(candles) > lookback:
                candles = candles[-lookback:]  # Slice the list to the last `lookback` elements

            if lookback is not None and len(candles) < lookback:
                return []

            if len(candles) < 2:
                return []

            # Extract data points
            opens = [candle.open for candle in candles]
            highs = [candle.high for candle in candles]
            lows = [candle.low for candle in candles]
            close = [candle.close for candle in candles]

            n = len(highs)

            # Loop through the data and check 3 consecutive candles for FVGs
            for i in range(2, n):  # Start bei der 2. Kerze (Index 1)
                open1, high1, low1, close1 = opens[i - 2], highs[i - 2], lows[i - 2], close[i - 2]
                open2, high2, low2, close2 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1]
                open3, high3, low3, close3 = opens[i], highs[i], lows[i], close[i]

                if low2 < low1 < close2 and close3 > high2:
                    pdArray = PDArray(name=self.name,direction="Bullish",candles=[candles[i],candles[i-1],candles[-2]],timeframe=last_candle.timeframe)
                    pdArray.candles.append(candles[i])
                    pdArray.candles.append(candles[i-1])
                    pd_arrays.append(pdArray)
                if high2 > high1 > close2 and close3 < low2:
                    pdArray = PDArray(name=self.name,direction="Bearish",candles=[candles[i],candles[i-1],candles[-2]],timeframe=last_candle.timeframe)
                    pdArray.candles.append(candles[i])
                    pdArray.candles.append(candles[i-1])
                    pd_arrays.append(pdArray)
        except Exception as e:
            logger.error("Orderblock Error: " + str(e))
        finally:
            return pd_arrays