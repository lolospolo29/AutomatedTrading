import pytz

from Interfaces.RiskManagement.ITimeWindow import ITimeWindow

berlinTimezone = pytz.timezone('Europe/Berlin')


class LondonMacroFX(ITimeWindow):
    def IsInExitWindow(self,time):
        pass

    def IsInEntryWindow(self,time):
        current_hour = time.hour
        current_minute = time.minute

        if current_minute >= 33  and  9 > current_hour >= 7:
            return True

        if 30 >= current_minute >= 3 and 9 == current_hour :
            return True

        return False
