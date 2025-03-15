from pydantic import BaseModel

from files.models.asset.Relation import Relation
from files.models.frameworks.FrameWork import FrameWork
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.Structure import Structure
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class RiskProfile(BaseModel):
    relation:Relation
    current_quarter:dict[int,int]
    market_maker_direction:dict[int,str]
    daily_profile:str
    weekly_profile:str
    monthly_profile:str
    current_htf_pd:dict[int, PDArray]
    frameworks_in_stdv_range:dict[int,list[FrameWork]]
    smt_detected:list[Structure]
    atr:dict[int, float]
    potential_no_trade_conditions:list
    news:list[NewsEvent]
    exchange_rate_breakeven:float=None
    bonds_percentage:float=None
    yields:float=None
    interest_rate:float=None
    funding_rate:float=None
