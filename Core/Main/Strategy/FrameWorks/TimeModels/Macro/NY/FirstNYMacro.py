from Interfaces.Strategy.ITimeWindow import ITimeWindow

# AM Macro
class FirstNYMacro(ITimeWindow):
    def IsInExitWindow(self,time):
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time):
        current_hour = time.hour
        current_minute = time.minute

        if (50 <= current_minute  and current_hour == 13) or (10 >= current_minute and current_hour == 14) :
            return True

        return False
