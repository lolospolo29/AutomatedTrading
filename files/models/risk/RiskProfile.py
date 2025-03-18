from pydantic import BaseModel

from files.models.frameworks.FrameWork import FrameWork
from files.models.frameworks.PDArray import PDArray
from files.models.frameworks.Structure import Structure
from files.models.risk.Fundamentals import Fundamentals
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class RiskProfile(BaseModel):
    risk_profile_id:str
    status:str
    current_quarter:str
    weekly_hedging:str
    daily_hedging:str
    daily_profile:str
    weekly_profile:str
    current_htf_pd:list[PDArray]
    stdv_frameworks:list[FrameWork]
    smt_detected:dict[int,list[Structure]]
    atr:float
    potential_no_trade_conditions:list
    news:list[NewsEvent]
    fundamentals:Fundamentals
