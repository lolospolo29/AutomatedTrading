from typing import Optional

from pydantic import BaseModel, Field


class Fundamentals(BaseModel):
    exchange_rate_breakeven:Optional[float]=Field(default=None, alias='exchangeRateBreakeven')
    bonds_percentage:Optional[float]=Field(default=None, alias='bondPercentage')
    yields:Optional[float]
    interest_rate:Optional[float]=Field(default=None, alias='interestRate')
    funding_rate:Optional[float]=Field(default=None, alias='fundingRate')