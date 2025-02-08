from app.interfaces.framework.IPDArray import IPDArray
from app.models.asset.Candle import Candle
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.frameworks.PDArray import PDArray
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum
from app.monitoring.logging.logging_startup import logger


class RejectionBlock(IPDArray):

    def __init__(self, lookback):
        self.lookback = lookback
        self.name = "RB"

    def return_entry(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode) -> float:
        try:
            low,high = self.return_candle_range(pd_array)
            if order_direction.BUY:
                if risk_mode.AGGRESSIVE:
                    return high

            if order_direction.SELL:
                if risk_mode.AGGRESSIVE:
                    return low

            if risk_mode.MODERAT or risk_mode.SAFE:
                return (low + high) / 2
        except Exception as e:
            logger.error("Rejection Block Entry Error with Exception"+str(e))


    def return_stop(self, pd_array: PDArray, order_direction: OrderDirectionEnum, risk_mode: RiskMode):
        try:
            low,high = self.return_candle_range(pd_array)
            if order_direction.BUY:
                if risk_mode.SAFE:
                    return low

            if order_direction.SELL:
                if risk_mode.SAFE:
                    return high

            if risk_mode.MODERAT or risk_mode.AGGRESSIVE:
                return (low + high) / 2
        except Exception as e:
            logger.error("Rejection Block Stop Error with Exception"+str(e))

    def return_candle_range(self, pd_array: PDArray) -> tuple[float, float]:
        """
        Returns the high and low of the RB Whick.

        :param pd_array: A PDArray object that contains candles.
        :return: A dictionary containing the range {'low': ..., 'high': ...}.
        """
        try:
            # Extract prices from the candles
            highs = [candle.high for candle in pd_array.candles]
            lows = [candle.low for candle in pd_array.candles]
            opens = [candle.open for candle in pd_array.candles]
            closes = [candle.close for candle in pd_array.candles]

            if pd_array.direction == "Bullish":
                low = min(lows)
                high = float(min(opens,closes))
                return low,high
            if pd_array.direction == "Bearish":
                low = float(max(opens,closes))
                high = float(max(highs))
                return low,high
        except Exception as e:
            logger.error("Rejection Block Candle Range Error with Exception"+str(e))

    def return_array_list(self, candles: list[Candle]) -> list:
        rejection_blocks = []

        try:
            if len(candles) < self.lookback:
                return []
            # We assume 'data_points_asset' contains the asset data (high, low, open, close, ids)
            opens = [candle.open for candle in candles]
            highs = [candle.high for candle in candles]
            lows = [candle.low for candle in candles]
            close = [candle.close for candle in candles]

            if len(opens) < self.lookback:
                return rejection_blocks  # Not enough data for rejection block detection

            for i in range(9, len(opens)):  # Start from the 10th candle onwards
                # Calculate average range of the previous 10 candles
                avg_range = sum([highs[j] - lows[j] for j in range(i - 9, i + 1)]) / 10

                # Current candle details
                open_price = opens[i]
                high_price = highs[i]
                low_price = lows[i]
                close_price = close[i]

                # Calculate the wicks
                upper_wick = high_price - max(open_price, close_price)
                lower_wick = min(open_price, close_price) - low_price

                # Bullish rejection: Large lower wick compared to average range
                if  lower_wick > avg_range:
                    rejection_blocks = PDArray(name=self.name,direction= "Bullish",candles=candles[i-9:i+1])
                    rejection_blocks.candles.append(candles[i])
                # Bearish rejection: Large upper wick compared to average range
                elif upper_wick > avg_range:
                    rejection_blocks = PDArray(name=self.name, direction="Bearish",candles=candles[i-9:i+1])
                    rejection_blocks.candles.append(candles[i])
        except Exception as e:
            logger.error("Rejection Block Exception {}".format(e))
        finally:
            return rejection_blocks
