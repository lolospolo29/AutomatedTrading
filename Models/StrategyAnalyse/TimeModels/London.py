import pytz

from Interfaces.RiskManagement.ITimeWindow import ITimeWindow

berlinTimezone = pytz.timezone('Europe/Berlin')


class LondonOpen(ITimeWindow):
    def IsInExitWindow(self,time) -> bool :
        if  13 >= time.hour >= 7 :
            return True
        return False

    def IsInEntryWindow(self,time) -> bool:
        if  10 >= time.hour >= 7 :
            return True
        return False
