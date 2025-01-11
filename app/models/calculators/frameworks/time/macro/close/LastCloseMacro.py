# PM Macro
from app.interfaces.framework.ITimeWindow import ITimeWindow


class LastCloseMacro(ITimeWindow):
    def IsInExitWindow(self,time):
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time):
        current_hour = time.hour
        current_minute = time.minute

        if 45 <= current_minute < 15 and current_hour == 20 :
            return True

        return False
