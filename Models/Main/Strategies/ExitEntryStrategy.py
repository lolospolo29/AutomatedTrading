from Interfaces.Strategy.IExitEntryStrategy import IExitEntryStrategy


class ExitEntryStrategy(IExitEntryStrategy):
    def __init__(self, name):
        self.name = name

    def applyRules(self):
        pass

    def setCallback(self, callback):
        pass

    def setPDArrays(self, PDArrays):
        pass