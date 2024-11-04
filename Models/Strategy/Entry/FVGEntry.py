from Interfaces.Strategy.IExitEntryStrategy import IExitEntryStrategy


class FVGEntry(IExitEntryStrategy):
    def __init__(self, name):
        self.name = name
        self.PDArrays = None  # PD arrays injected from main strategy
        self.callback = None  # This will hold the reference to the callback function

    def setPDArrays(self, PDArrays):
        self.PDArrays = PDArrays

    def setCallback(self, callback):
        """
        This method sets the callback that the Strategy class provides.
        """
        self.callback = callback

    def applyRules(self):
        """
        Apply the exit rules and potentially update PD arrays.
        If PD arrays are updated, notify the Strategy class using the callback.
        """
        # Example: new PD array calculated based on exit rules logic
        new_pd_array = [5, 6, 7, 8]  # Just a dummy example of a PD array
        if self.callback:
            # Call the callback function, passing the new PD array to the Strategy
            self.callback(new_pd_array)
        return True  # Example: return True if exit conditions are met
