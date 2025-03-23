from typing import Optional

from pydantic import BaseModel, Field

from files.helper.mediator.PriceMediator import PriceMediator
from files.models.frameworks.Structure import Structure
from files.models.risk.Fundamentals import Fundamentals
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class RiskProfileInput(BaseModel):
    quarter:Optional[str]=Field(default=None)
    mediator:PriceMediator = Field(default=None,exclude=True)
    news:list[NewsEvent] = Field(default=None,exclude=True)
    fundamentals:Fundamentals = Field(default=None,exclude=True)
    smt:Structure = Field(default=None,exclude=True)