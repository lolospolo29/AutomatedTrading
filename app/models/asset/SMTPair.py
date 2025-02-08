from pydantic import BaseModel


class SMTPair(BaseModel):
    strategy: str
    asset_a:str
    asset_b:str
    correlation: str
