from app.interfaces.framework.ITimeWindow import ITimeWindow


class FirstLondonMacro(ITimeWindow):
    def IsInExitWindow(self,time):
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time):
        current_hour = time.hour
        current_minute = time.minute

        if current_minute >= 33  and current_hour == 7:
            return True

        return False
