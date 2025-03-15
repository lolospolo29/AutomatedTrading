from files.interfaces.ITimeWindow import ITimeWindow


class Asia(ITimeWindow):

    def is_in_exit_window(self, time) -> bool:
        return self.is_in_entry_window(time)

    @staticmethod
    def is_in_entry_window(time) -> bool:
        if 4 > time.hour >= 0 or time.hour >= 12:
            return True
        return False