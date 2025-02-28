from app.helper.calculator.framework.pdarray.PDEnum import PDEnum
from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class BPR(IPDArray):
    """ICT Balanced price range (BPR) is the area on price chart where two opposite fair value gaps overlap"""

    def __init__(self):
        self.name = PDEnum.BPR.value

    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        """
        BPR Entry has different Modes
        returns the between High and Low based on Direction
        Moderat: returns the 50% Range of the Candle of the PDArray
        """
        try:
            low, high = self.return_candle_range(pd_array)
            if order_direction.BUY:
                if risk_mode.SAFE:
                    return low
                if risk_mode.AGGRESSIVE:
                    return high

            if order_direction.SELL:
                if risk_mode.SAFE:
                    return low
                if risk_mode.AGGRESSIVE:
                    return high

            if risk_mode.MODERAT:
                return (low + high) / 2
        except Exception as e:
            logger.error("BPR Entry Calculation Exception: {}".format(e))

    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, riskMode: RiskMode) -> float:
        try:
            highs = [candle.high for candle in pd_array.candles]
            lows = [candle.low for candle in pd_array.candles]
            close = [candle.close for candle in pd_array.candles]
            open = [candle.open for candle in pd_array.candles]

            if order_direction.BUY:
                if riskMode.SAFE:
                    return min(lows)
                if riskMode.MODERAT:
                    return min(open)
                if riskMode.AGGRESSIVE:
                    return min(close)
            if order_direction.SELL:
                if riskMode.SAFE:
                    return max(highs)
                if riskMode.MODERAT:
                    return max(open)
                if riskMode.AGGRESSIVE:
                    return max(close)
        except Exception as e:
            logger.error("BPR Stop Calculation Exception: {}".format(e))

    def return_candle_range(self, pd_array: PDArray) -> tuple[float, float]:
        """
        Returns the gap between two Fair Value Gaps (FVGs) within the Balanced Price Range (BPR).

        :param : List of Candle objects.
        :param pd_array: A PDArray object that contains the IDs of the six candles forming the BPR.
        :return: A Tuple containing the gap range {'low': ..., 'high': ...}.
        """
        # Retrieve the candles corresponding to the IDs in pdArray
        try:

            # Extract prices from the candles
            highs = [candle.high for candle in pd_array.candles]
            lows = [candle.low for candle in pd_array.candles]

            # Identify the FVGs from the first 3 and the last 3 candles
            bearish_fvg_high = max(lows[:3])  # Bearish FVG range (first three candles)
            bearish_fvg_low = min(highs[:3])

            bullish_fvg_high = max(lows[3:])  # Bullish FVG range (last three candles)
            bullish_fvg_low = min(highs[3:])

            # Calculate the gap based on the direction of the BPR
            gap_high = min(bullish_fvg_high, bearish_fvg_high)
            gap_low = max(bullish_fvg_low, bearish_fvg_low)

            # Return the gap range
            return gap_low, gap_high
        except Exception as e:
            logger.error("BPR Return Candle Range Exception: {}".format(e))

    def return_array_list(self, candles: list[Candle]) -> list[PDArray]:
        """
        Calculates Balanced Price Ranges using 2 FVGs Overlapping
        :param candles:
        :return:
        """
        if len(candles) < 6:
            return []

        pd_arrays = []
        try:
            # Lists to store identified FVGs
            bearish_fvg_list = []
            bullish_fvg_list = []

            opens = [candle.open for candle in candles]
            highs = [candle.high for candle in candles]
            lows = [candle.low for candle in candles]
            close = [candle.close for candle in candles]

            n = len(opens)

            # First step: Identify all Fair Value Gaps (FVGs)
            for i in range(2, n):  # Start from the 3rd candle (index 2)
                open1, high1, low1, close1 = opens[i - 2], highs[i - 2], lows[i - 2], close[i - 2]
                open2, high2, low2, close2 = opens[i - 1], highs[i - 1], lows[i - 1], close[i - 1]
                open3, high3, low3, close3 = opens[i], highs[i], lows[i], close[i]

                # Check for Bearish FVG (Sell-side FVG)
                if low1 > high3 and close2 < low1:
                    bearish_fvg_list.append({
                        'high': low1,  # Top of FVG range
                        'low': high3,  # Bottom of FVG range
                        'candles': [candles[i], candles[i - 1], candles[i - 2]],
                        'index': [i, i - 1, i - 2]
                    })

                # Check for Bullish FVG (Buy-side FVG)
                if high1 < low3 and close2 > high1:
                    bullish_fvg_list.append({
                        'high': low3,  # Top of FVG range
                        'low': high1,  # Bottom of FVG range
                        'candles': [candles[i], candles[i - 1], candles[i - 2]],
                        'index': [i, i - 1, i - 2]
                    })

            # Second step: Check for overlaps between Bearish and Bullish FVGs
            for sell_fvg in bearish_fvg_list:
                for buy_fvg in bullish_fvg_list:
                    # Check for overlap between the two FVGs
                    overlapLow = max(sell_fvg['low'], buy_fvg['low'])
                    overlapHigh = min(sell_fvg['high'], buy_fvg['high'])

                    if overlapLow < overlapHigh:
                        # There is an overlap, create a Balanced Price Range (BPR)

                        # Determine the direction based on the order of the FVGs
                        direction = "Bullish"  # Default direction is bullish

                        # If the first FVG (sell_fvg) is Bearish and the second (buy_fvg) is Bullish
                        if max(sell_fvg['index']) < max(buy_fvg['index']):
                            direction = "Bullish"
                        # If the first FVG (buy_fvg) is Bullish and the second (sell_fvg) is Bearish
                        if max(sell_fvg['index']) > max(buy_fvg['index']):
                            direction = "Bearish"

                        fvgs_candles = sell_fvg['candles']
                        fvgs_candles.extend(buy_fvg['candles'])

                        pdArray = PDArray(name=self.name, direction=direction,candles=fvgs_candles)

                        pd_arrays.append(pdArray)
        except Exception as e:
            logger.error("Balanced Price Range Calculation Exception: {}".format(e))
        finally:
            return pd_arrays
