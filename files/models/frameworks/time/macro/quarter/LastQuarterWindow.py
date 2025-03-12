from files.interfaces.ITimeWindow import ITimeWindow


class LastQuarterWindow(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        current_minute = time.minute

        if 0 <= current_minute <= 10 or 59 >= current_minute >= 50:
            return True

        return False