class ExpectedTimeFrame:
    def __init__(self, timeframe, maxLen):
        self.timeframe = timeframe
        self.max_Len = maxLen

    def to_dict(self) -> dict:
        return {
            "ExpectedTimeFrame": {
                "timeframe": self.timeframe,
                "maxLen": self.max_Len,
            }
        }