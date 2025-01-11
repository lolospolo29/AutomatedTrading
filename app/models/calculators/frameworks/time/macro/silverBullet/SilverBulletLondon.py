from app.interfaces.framework.ITimeWindow import ITimeWindow


# SB Macro
class SecondNYMacro(ITimeWindow):
    def IsInExitWindow(self,time):
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time):
        current_hour = time.hour
        current_minute = time.minute

        if 8 <= current_hour < 9 :
            return True

        return False
