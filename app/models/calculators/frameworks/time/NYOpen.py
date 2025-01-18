from app.interfaces.framework.ITimeWindow import ITimeWindow


class NYOpen(ITimeWindow):
    def is_in_exit_window(self, time) -> bool:
        return self.is_in_entry_window(time)
    def is_in_entry_window(self, time) -> bool:
        if  15 >= time.hour >= 12 :
            return True
        return False
