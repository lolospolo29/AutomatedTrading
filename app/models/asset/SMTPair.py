from pydantic import BaseModel


class SMTPair(BaseModel):
    strategy: str
    smt_pairs: list[str]
    correlation: str
