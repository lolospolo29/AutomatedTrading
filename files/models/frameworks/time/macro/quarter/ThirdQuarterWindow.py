from files.interfaces.ITimeWindow import ITimeWindow


class ThirdQuarterWindow(ITimeWindow):

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        current_minute = time.minute

        if 40 <= current_minute <= 50:
            return True

        return False