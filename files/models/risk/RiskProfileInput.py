from pydantic import BaseModel

from files.helper.mediator.PriceMediator import PriceMediator
from files.models.risk.Fundamentals import Fundamentals
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class RiskProfileInput(BaseModel):
    mediator:PriceMediator
    news:list[NewsEvent]
    fundamentals:Fundamentals