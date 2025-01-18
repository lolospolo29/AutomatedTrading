from app.interfaces.framework.ITimeWindow import ITimeWindow


# PM Macro
class FirstCloseMacro(ITimeWindow):
    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        current_hour = time.hour
        current_minute = time.minute

        if 50 >= current_minute >= 10  and current_hour == 18 :
            return True

        return False
