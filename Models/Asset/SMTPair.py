class SMTPair:
    def __init__(self, strategy: str, smtPairs: list[str], correlation: str):
        self.strategy: str = strategy
        self.smtPairs: list[str] = smtPairs
        self.correlation: str = correlation
