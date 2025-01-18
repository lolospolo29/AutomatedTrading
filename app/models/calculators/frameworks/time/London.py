from app.interfaces.framework.ITimeWindow import ITimeWindow


class LondonOpen(ITimeWindow):
    def is_in_exit_window(self, time) -> bool :
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time) -> bool:
        if  10 >= time.hour >= 7 :
            return True
        return False
