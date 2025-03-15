from files.interfaces.ITimeWindow import ITimeWindow


class FirstLondonMacro(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        current_hour = time.hour
        current_minute = time.minute

        if current_minute >= 33 and current_hour == 6:
            return True

        return False
