from files.models.risk.Fundamentals import Fundamentals
from files.models.risk.RiskProfile import RiskProfile
from files.models.risk.RiskProfileInput import RiskProfileInput


class RiskProfileAnalyzer:
    def update_risk_profile(self,risk_profile:RiskProfile, risk_input:RiskProfileInput)->RiskProfile:

        if risk_input.fundamentals:
            risk_profile = self._update_fundamentals(risk_profile, risk_input.fundamentals)

        if risk_input.news:
            if len(risk_profile.news) > 3:
                risk_profile.news = risk_input.news

        return risk_profile

    @staticmethod
    def _update_fundamentals(risk_profile:RiskProfile, fundamentals:Fundamentals)->RiskProfile:
        if fundamentals.yields:
            risk_profile.fundamentals.yields = fundamentals.yields
        if fundamentals.funding_rate:
            risk_profile.fundamentals.funding_rate = fundamentals.funding_rate
        if fundamentals.interest_rate:
            risk_profile.fundamentals.interest_rate = fundamentals.interest_rate
        if fundamentals.exchange_rate_breakeven:
            risk_profile.fundamentals.exchange_rate_breakeven = fundamentals.exchange_rate_breakeven
        if fundamentals.bonds_percentage:
            risk_profile.fundamentals.bonds_percentage = fundamentals.bonds_percentage

        return risk_profile