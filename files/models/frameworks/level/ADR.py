class ADR:
    @staticmethod
    def calculate_adr(high:float,low:float)->float:
        return abs(high-low)