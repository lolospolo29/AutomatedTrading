from Interfaces.RiskManagement.ITechnicalStop import ITechnicalStop


class BreakEven(ITechnicalStop):
    def __init__(self, percentage):
        self.percentage = percentage

    def moveExit(self):
        pass
