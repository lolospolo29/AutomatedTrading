from Interfaces.RiskManagement.ITimeWindow import ITimeWindow

class LondonOpen(ITimeWindow):
    def IsInExitWindow(self,time) -> bool :
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time) -> bool:
        if  10 >= time.hour >= 7 :
            return True
        return False
