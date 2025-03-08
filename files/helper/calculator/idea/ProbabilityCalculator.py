from files.models.frameworks.Level import Level
from files.models.frameworks.PDArray import PDArray


class ProbabilityCalculator:
    """
    Calculates the probability of hitting Take Profit (TP) based on price levels,
    premium/discount zones, and market structure.
    """
    def __init__(self, entry_price: float, take_profit: float, pd_arrays: list[PDArray], levels: list[Level]):
        self.entry_price = entry_price
        self.take_profit = take_profit
        self.pd_arrays = pd_arrays
        self.levels = levels
        self.probability_score = 0  # Score to determine probability classification

    def evaluate_probability(self) -> str:
        """Calculates probability of hitting TP and classifies it as Low, Medium, or High."""
        self._analyze_premium_discount_zone()
        self._analyze_levels()

        # Define probability classification based on score
        if self.probability_score >= 8:
            return "High"
        elif self.probability_score >= 4:
            return "Medium"
        else:
            return "Low"

    def _analyze_premium_discount_zone(self):
        """Adjusts probability based on whether TP is in a favorable discount/premium zone."""
        for pd in self.pd_arrays:
            if pd.is_premium_zone() and self.take_profit < self.entry_price:
                self.probability_score += 3  # Favorable for shorts
            elif pd.is_discount_zone() and self.take_profit > self.entry_price:
                self.probability_score += 3  # Favorable for longs

    def _analyze_levels(self):
        """Analyzes how many levels are supporting or opposing the TP move."""
        for level in self.levels:
            if self.entry_price < self.take_profit and level.price > self.entry_price:
                self.probability_score += 2  # Support for longs
            elif self.entry_price > self.take_profit and level.price < self.entry_price:
                self.probability_score += 2  # Support for shorts
            else:
                self.probability_score -= 1  # Opposing level (resistance for longs, support for shorts)
