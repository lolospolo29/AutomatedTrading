from typing import Optional

from pydantic import BaseModel

from app.models.asset.Relation import Relation
from app.models.asset.CandleSeries import CandleSeries
from app.models.asset.SMTPair import SMTPair


class Asset(BaseModel):

    name:str
    asset_class:str
    brokers:Optional[list] = None
    strategies:Optional[list[str]] = None
    smt_pairs:Optional[list[SMTPair]] = None
    relations:Optional[list[Relation]] = None
    candles_series:Optional[list[CandleSeries]] = None
