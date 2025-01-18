from app.interfaces.framework.ITimeWindow import ITimeWindow


class Asia(ITimeWindow):
    def is_in_exit_window(self, time) -> bool:
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time) -> bool:
        if  5 >= time.hour >= 0 :
            return True
        return False
