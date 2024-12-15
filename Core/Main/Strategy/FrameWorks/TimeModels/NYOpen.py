from Interfaces.Strategy.ITimeWindow import ITimeWindow

class NYOpen(ITimeWindow):
    def IsInExitWindow(self,time) -> bool:
        return self.IsInEntryWindow(time)
    def IsInEntryWindow(self,time) -> bool:
        if  15 >= time.hour >= 12 :
            return True
        return False
