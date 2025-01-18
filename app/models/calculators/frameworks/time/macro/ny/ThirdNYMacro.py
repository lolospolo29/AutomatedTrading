from app.interfaces.framework.ITimeWindow import ITimeWindow


# AM Macro
class ThirdNYMacro(ITimeWindow):
    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        current_hour = time.hour
        current_minute = time.minute

        if (50 <= current_minute  and current_hour == 15) or (10 >= current_minute and current_hour == 16) :
            return True

        return False
