class SMTPair:
    def __init__(self, strategy: str, smtPair: list[str], correlation: str):
        self.strategy: str = strategy
        self.smt_pairs: list[str] = smtPair
        self.correlation: str = correlation

    def to_dict(self) -> dict:
        return {
            "SMTPair": {
                "strategy": self.strategy,
                "smt_pairs": self.smt_pairs,
                "correlation": self.correlation
            }
        }