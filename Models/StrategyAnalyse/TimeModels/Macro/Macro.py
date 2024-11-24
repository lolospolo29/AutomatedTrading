from Interfaces.RiskManagement.ITimeWindow import ITimeWindow


class Macro(ITimeWindow):
    def IsInEntryWindow(self,time):

        # Get current hour and minute
        current_hour = time.hour
        current_minute = time.minute

        # Check first time window (xx:50 to xx:10)
        if current_minute >= 50 or current_minute < 10:
            return True

        # Check second time window (xx:20 to xx:40)
        if 20 <= current_minute < 40:
            return True

        return False

    def IsInExitWindow(self):
        pass

