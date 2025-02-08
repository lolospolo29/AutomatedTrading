from typing import Tuple, Any

from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.calculators.entry.orderWeightage.OrderWeightage import OrderWeightage
from app.models.calculators.entry.ratio.BaseRatio import BaseRatio
from app.models.calculators.entry.ratio.FixedRatio import FixedRatio
from app.models.calculators.entry.ratio.RangeRatio import RangeRatio
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum


# noinspection PyTypeChecker
class ProfitStopEntryCalculator:
    """
    RiskCalculator is a singleton class designed to manage and calculate risk across various
    financial trading strategies. It provides a comprehensive suite of methods for calculating
    risk parameters, such as profits, stops, entry points, and invalidation scenarios, based on
    different trading ratios, scenarios, and directional inputs.

    This class integrates several components to handle specific aspects of risk evaluation:
    `OrderWeightage`, `BaseRatio`, `FixedRatio`, `RangeRatio`, `InvalidationClose`,
    `InvalidationSteady`, `BreakEven`, `TrailingStop`, and others. By leveraging these
    components, it supports single and list inputs for fixed and range-based ratios, checks
    invalidation for exit, and calculates trailing stops and breakeven scenarios, among other
    functions. It is intended for use in automated trading systems or similar applications
    where calculated risk metrics determine trading actions.

    :ivar _order_weightage: Instance of `OrderWeightage` for handling proportional adjustments.
    :type _order_weightage: OrderWeightage
    :ivar _base_ratio: Instance of `BaseRatio` for core profit-stop calculations.
    :type _base_ratio: BaseRatio
    :ivar _fixed_ratio: Instance of `FixedRatio` for consistent ratio-based calculations.
    :type _fixed_ratio: FixedRatio
    :ivar _range_ratio: Instance of `RangeRatio` for calculations involving multiple range inputs.
    :type _range_ratio: RangeRatio
    :ivar _initialized: Boolean flag indicating whether the singleton is initialized.
    :type _initialized: bool
    """
    # region Initializing
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProfitStopEntryCalculator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self._order_weightage = OrderWeightage()
            self._base_ratio = BaseRatio()
            self._fixed_ratio = FixedRatio()
            self._range_ratio = RangeRatio()
            self._initialized: bool = True  # Mark as initialized
    # endregion

    # region Order Weightage

    def set_order_weightage_percent(self, entries:list[ProfitStopEntry], mode: RiskMode) -> list[ProfitStopEntry]:
        """
        Adjusts the weightage percentages for the given entries based on the specified
        risk mode. This method modifies the input `entries` with updated percentages
        and returns the modified list of entries.

        :param entries: A list of `ProfitStopEntry` instances representing the entries
            for which weightage percentages need to be set.
        :param mode: The `RiskMode` that determines how percentages are calculated.
        :return: A list of `ProfitStopEntry` instances with updated weightage percentages.
        """
        return self._order_weightage.set_percentages_based_on_mode(entries, mode)


    # endregion

    # region Single Base Ratio Input
    def calculate_base_profit(self, entry:float, stop: float, ratio: float) -> float:
        """
        Calculates the base profit using the given entry price, stop price, and profit-loss ratio.
        This function provides a foundation for profit calculation based on the ratio between potential
        profit and loss.

        :param entry: The entry price for the trade at which the calculation begins.
        :type entry: float
        :param stop: The stop-loss price for the trade below which the position is exited.
        :type stop: float
        :param ratio: The risk-to-reward ratio used for profit estimation.
        :type ratio: float
        :return: The calculated base profit based on the provided parameters.
        :rtype: float
        """
        return self._base_ratio.calculate_profit(entry, stop, ratio)

    def calculate_base_stop(self, entry:float, profit: float, ratio: float) -> float:
        """
        Calculates the base stop value using the entry price, target profit, and the risk-reward ratio.

        This function computes the stop-loss value based on the given entry price, expected
        profit value, and a specified risk-reward ratio. It internally uses the `_base_ratio`
        object's `calculate_stop` method to perform the actual calculation. The method assumes
        all input parameters are valid numeric types.

        :param entry: The entry price for the trade.
        :param profit: The target profit value for the trade.
        :param ratio: The risk-reward ratio for the trade.
        :return: The calculated base stop price.
        :rtype: float
        """
        return self._base_ratio.calculate_stop(entry, profit, ratio)

    def calculate_base_entry(self, stop:float, profit:float, ratio:float) -> float:
        """
        Calculate the base entry point for a financial strategy based on stop-loss, profit, and ratio values.

        This function utilizes the `_base_ratio` attribute's `calculate_entry` method to compute the
        desired base entry point. It assumes input parameters represent valid numerical values
        commonly used in financial models.

        :param stop: The stop-loss value to be used in the calculation.
        :type stop: float
        :param profit: The profit target value for the calculation.
        :type profit: float
        :param ratio: The risk-reward ratio associated with the strategy.
        :type ratio: float
        :return: The computed base entry value.
        :rtype: float
        """
        return self._base_ratio.calculate_entry(stop, profit, ratio)
    # endregion

    # region  Single Fixed Ratio Input

    def calculate_fixed_profit(self, entry: float, stop: float, ratio: float, direction: OrderDirectionEnum)->Tuple[Any,bool]:
        """
        Calculate the fixed profit level based on the entry price, stop-loss price, risk-reward
        ratio, and trade direction.

        This method computes the profit level a trade needs to reach to achieve a specified
        risk-reward ratio. It uses the entry price, stop-loss price, ratio, and trade
        direction for calculation. The result includes the calculated profit level and a
        boolean indicating whether the profit is properly computed.

        :param entry: The entry price of the trade.
        :param stop: The stop-loss price for the trade.
        :param ratio: The desired risk-reward ratio.
        :param direction: The trade direction, either long or short, defined by
            OrderDirectionEnum.
        :return: A tuple where the first element is the fixed profit level (or relevant
            value), and the second element is a boolean to indicate success of the
            calculation.
        """
        return self._fixed_ratio.calculate_fixed_profit(entry, stop, ratio, direction)

    def calculate_fixed_ratio_stop(self, entry: float, profit: float, ratio: float, direction: OrderDirectionEnum)->Tuple[Any,bool]:
        """
        Calculate the fixed ratio stop for a given trade setup.

        The fixed ratio stop calculation determines the stop-loss level for a trade
        based on the entry price, projected profit, and a specified fixed risk-reward
        ratio. The direction of the trade (buy or sell) is also considered in the
        calculation.

        :param entry: The entry price for the trade.
        :param profit: The projected profit level for the trade.
        :param ratio: The risk-reward ratio used to calculate the stop level.
        :param direction: The direction of the trade, either buy or sell,
            specified as an instance of OrderDirectionEnum.
        :return: A tuple where the first element represents the calculated fixed
            ratio stop price (type could vary, hence Any), and the second element
            is a boolean indicating if the calculation was successful.
        """
        return self._fixed_ratio.calculate_fixed_ratio_stop(entry, profit, ratio, direction)

    def calculate_fixed_entry(self, stop: float, profit: float, ratio: float, direction: OrderDirectionEnum)->Tuple[Any,bool]:
        """
        Calculates the fixed entry point for an order based on the specified stop loss, profit target,
        risk-to-reward ratio, and trading direction. This method delegates the calculation logic to an
        underlying implementation defined in the `_fixed_ratio` attribute.

        :param stop: The stop loss value for the trade in the specified trading instrument's units.
        :param profit: The profit target for the trade in the specified trading instrument's units.
        :param ratio: The risk-to-reward ratio value, representing the desired reward for a given unit of risk.
        :param direction: The trading direction, which specifies whether the trade is a buy or sell order.
        :return: A tuple containing the calculated entry point value and a boolean flag indicating success.
        """
        return self._fixed_ratio.calculate_fixed_entry(stop, profit, ratio, direction)
    # endregion

    # region List Fixed Ratio Input
    def calculate_profits_fixed(self, entries: list[float], stops: list[float], ratio: float,
                                direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        """
        Calculates profits based on fixed ratio logic using the provided entries, stops, ratio,
        and trade direction. This function processes a fixed ratio strategy where
        each profit level and stop level is calculated to maximize or minimize profit
        based on the given parameters.

        :param entries: List of entry prices for trades.
        :param stops: List of stop prices corresponding to each entry price.
        :param ratio: Fixed profit ratio to apply, expressed as a floating-point number.
        :param direction: Direction of the order, defined by the OrderDirectionEnum.

        :return: A list of ProfitStopEntry objects, each representing calculated profit
                 and stop levels based on the given entries, stops, and ratio.
        """
        return self._fixed_ratio.calculate_profits(entries, stops, ratio, direction)

    def calculate_stops_fixed(self, entries: list[float], profits: list[float], ratio: float,
                              direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        """
        Calculates profit and stop loss points for a given set of entries, profits, ratio
        and trade direction using a fixed ratio approach. The function relies on an
        underlying implementation to compute these values and returns a list of
        `ProfitStopEntry` objects containing calculated stops.

        :param entries: List of entry point prices for the trades.
        :type entries: list[float]
        :param profits: List of target profit prices for the trades.
        :type profits: list[float]
        :param ratio: Risk-to-reward ratio to use in calculating stop loss values.
        :type ratio: float
        :param direction: The trading direction indicating long or short positions.
        :type direction: OrderDirectionEnum
        :return: List of `ProfitStopEntry` objects with calculated stop and profit points.
        :rtype: list[ProfitStopEntry]
        """
        return self._fixed_ratio.calculate_stops(entries, profits, ratio, direction)

    def calculate_entries_fixed(self, stops: list[float], profits: list[float], ratio: float,
                                direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        """
        Calculate profitable entries based on fixed risk-reward ratio.

        This method uses a fixed ratio strategy to calculate potential entries
        for trades by analyzing provided stops and profit levels. It leverages
        the direction of the order to determine alignment with the market
        conditions and ensures detailed calculation for each scenario.

        :param stops: A list of stop-loss levels which signify the maximum loss
                      acceptable for each trade.
        :param profits: A list of profit targets which denote the exit levels
                        where trades would ideally close with profit.
        :param ratio: Risk-reward ratio that determines the proportional
                      relationship between potential loss and gain for trades.
        :param direction: The direction (buy/sell) of the order as an
                          enumeration value of OrderDirectionEnum.
        :return: A list of calculated entries, each represented as a
                 ProfitStopEntry object containing the associated stop-loss
                 and profit values.
        """
        return self._fixed_ratio.calculate_entries(stops, profits, ratio, direction)
    # endregion





    # region Single Range Ratio Input
    def calculate_range_profits(self, entry: float, stop: float, rangeRatio: list[float],
                                direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        """
        Calculates a sequence of profit and stop loss levels based on the given entry point,
        stop loss, range ratios, and direction.

        This function utilizes the range ratio to derive specific profit and stop levels.
        It is particularly useful for scenarios where dynamic risk-to-reward levels
        need to be calculated in trading strategies.

        :param entry: The entry price for the trade.
        :type entry: float
        :param stop: The stop loss price for the trade.
        :type stop: float
        :param rangeRatio: A list of floats representing range ratios to calculate profit levels.
        :type rangeRatio: list[float]
        :param direction: Indicates the trade direction (long or short) represented by an enum.
        :type direction: OrderDirectionEnum
        :return: A list of ProfitStopEntry objects containing calculated profit and stop levels.
        :rtype: list[ProfitStopEntry]
        """
        return self._range_ratio.calculate_range_profits(entry, stop, rangeRatio, direction)

    def calculate_range_stops(self, entry: float, profit: float, rangeRatio: list[float]
                              , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        """
        Calculates range-based stops for an order given the entry price, profit target,
        range ratios, and order direction. This function determines the appropriate stops
        by taking into account the specified range ratios and overall movement direction of
        the order.

        :param entry: Entry price of the order
        :param profit: Target profit for the order
        :param rangeRatio: List of range ratios to calculate stops for
        :param direction: Direction of the order (e.g., buy or sell)
        :return: List of ProfitStopEntry containing the calculated stops based on the
            input parameters
        """
        return self._range_ratio.calculate_range_stops(entry, profit, rangeRatio, direction)

    def calculate_range_entries(self, stop: float, profit: float, rangeRatio: list[float]
                                , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        """
        Calculates range-based entries for given trading parameters.

        This function uses the provided stop loss, profit target, range ratio,
        and order direction to compute and return a list of entries based on
        the specified range ratio. These entries represent profit and stop loss
        values configured for different trading scenarios according to the
        input parameters.

        :param stop: The stop loss value for the trade.
        :type stop: float
        :param profit: The profit target value for the trade.
        :type profit: float
        :param rangeRatio: A list of floating-point values representing the
            range ratio for calculating entries.
        :type rangeRatio: list[float]
        :param direction: The trading direction, which is specified as an
            enumerated value of OrderDirectionEnum.
        :type direction: OrderDirectionEnum
        :return: A list containing ProfitStopEntry objects, each representing
            a calculated trading entry based on the specified parameters.
        :rtype: list[ProfitStopEntry]
        """
        return self._range_ratio.calculate_range_entries(stop, profit, rangeRatio, direction)
    # endregion

    # region List Range Ratio Input
    def calculate_profits_range(self, entries: list[float], stops: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        """
        Calculates the profits within a specified range ratio for a given set of entry
        and stop values in the context of a specified order direction. This method
        utilizes the `_range_ratio` instance to compute the results.

        :param entries: List of entry prices.
        :type entries: list[float]
        :param stops: List of stop prices corresponding to the entry prices.
        :type stops: list[float]
        :param rangeRatio: List of range ratios to calculate the profits.
        :type rangeRatio: list[int]
        :param direction: The direction of the order, such as BUY or SELL, specified
            as an instance of OrderDirectionEnum.
        :type direction: OrderDirectionEnum
        :return: A list of ProfitStopEntry objects representing the computed profits
            and corresponding stop and entry values.
        :rtype: list[ProfitStopEntry]
        """
        return self._range_ratio.calculate_profits(entries, stops, rangeRatio, direction)

    def calculate_stops_range(self, entries: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        """
        Calculates the stop range for given entries, profits, range ratios, and a specified direction
        using the provided `_range_ratio` logic. The resulting calculation will output a list of
        `ProfitStopEntry` objects, which represent the stops determined based on the inputs and the
        calculation logic.

        :param entries: A list of entry prices.
        :param profits: A list of target profit values corresponding to the given entries.
        :param rangeRatio: A list of integer values used to define the ratio influencing stop
            calculations.
        :param direction: The direction of the order, specified as an instance of
            `OrderDirectionEnum`, determining whether the calculation is for buy or sell stops.
        :return: A list of `ProfitStopEntry` objects derived from the stop range calculation.
        """
        return self._range_ratio.calculate_stops(entries, profits, rangeRatio, direction)

    def calculate_entries_range(self, stops: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        """
        Calculates the range of potential entry points based on the provided stops, profits, range ratios,
        and the trading direction. The method utilizes a specific range ratio calculation logic to provide
        entry points tailored to the input parameters. It returns a list of computed entries containing
        profit and stop information.

        :param stops: A list of stop values where each stop defines the price level at which to
            exit a trade if the market moves unfavorably.
        :param profits: A list of profit values where each profit specifies the target levels for
            exiting a trade once the desired market conditions are met.
        :param rangeRatio: A list of integers that represent ratios applied to calculate the range of
            entry points based on defined stops and profits.
        :param direction: The direction of the order, which determines whether the calculation is for
            a long or short position. This parameter is of type ``OrderDirectionEnum``, and it ensures
            that the logic adapts based on the market movement aimed for.
        :return: A list of ``ProfitStopEntry`` objects indicating the computed entries for the provided
            stop and profit levels. Each entry encapsulates the related profit and stop points based on
            applied range ratios.
        :rtype: list[ProfitStopEntry]
        """
        return self._range_ratio.calculate_entries(stops, profits, rangeRatio, direction)
    # endregion