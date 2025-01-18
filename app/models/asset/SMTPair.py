class SMTPair:
    def __init__(self, strategy: str, smtPair: list[str], correlation: str):
        self.strategy: str = strategy
        self.smt_pairs: list[str] = smtPair
        self.correlation: str = correlation
