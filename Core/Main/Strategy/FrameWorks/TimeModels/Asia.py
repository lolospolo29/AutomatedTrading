from Interfaces.Strategy.ITimeWindow import ITimeWindow

class Asia(ITimeWindow):
    def IsInExitWindow(self,time) -> bool:
        return self.IsInEntryWindow(time)

    def IsInEntryWindow(self,time) -> bool:
        if  5 >= time.hour >= 0 :
            return True
        return False
