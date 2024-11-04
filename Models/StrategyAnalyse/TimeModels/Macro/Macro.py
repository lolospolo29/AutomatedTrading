from datetime import datetime

from Interfaces.RiskManagement.ITimeWindow import ITimeWindow


class Macro(ITimeWindow):
    def IsInEntryWindow(self):
        now = datetime.now()

        # Get current hour and minute
        current_hour = now.hour
        current_minute = now.minute

        # Check first time window (xx:50 to xx:10)
        if current_minute >= 50 or current_minute < 10:
            return True

        # Check second time window (xx:20 to xx:40)
        if 20 <= current_minute < 40:
            return True

        return False

    def IsInExitWindow(self):
        pass

