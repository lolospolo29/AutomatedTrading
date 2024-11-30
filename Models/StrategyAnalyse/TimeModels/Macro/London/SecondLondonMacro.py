from Interfaces.RiskManagement.ITimeWindow import ITimeWindow


class SecondLondonMacro(ITimeWindow):
    def IsInExitWindow(self,time):
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time):
        current_hour = time.hour
        current_minute = time.minute

        if 33 > current_minute >= 3  and current_hour == 9:
            return True

        return False
