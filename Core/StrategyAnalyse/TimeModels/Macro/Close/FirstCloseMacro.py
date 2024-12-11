from Interfaces.RiskManagement.ITimeWindow import ITimeWindow

# PM Macro
class FirstCloseMacro(ITimeWindow):
    def IsInExitWindow(self,time):
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time):
        current_hour = time.hour
        current_minute = time.minute

        if 50 >= current_minute >= 10  and current_hour == 18 :
            return True

        return False
