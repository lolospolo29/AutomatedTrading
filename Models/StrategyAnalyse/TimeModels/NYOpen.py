import pytz

from Interfaces.RiskManagement.ITimeWindow import ITimeWindow

berlinTimezone = pytz.timezone('Europe/Berlin')


class NYOpen(ITimeWindow):
    def IsInExitWindow(self,time) -> bool:
        if  15 >= time.hour >= 12 :
            return True
        return False

    def IsInEntryWindow(self,time) -> bool:
        if  15 >= time.hour >= 12 :
            return True
        return False
