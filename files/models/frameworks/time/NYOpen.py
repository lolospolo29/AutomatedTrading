from files.interfaces.ITimeWindow import ITimeWindow


class NYOpen(ITimeWindow):

    @property
    def name(self):
        return "NYOPEN"

    def is_in_exit_window(self, time) -> bool:
        return self.is_in_entry_window(time)

    @staticmethod
    def is_in_entry_window(time) -> bool:
        if 15 > time.hour >= 11:
            return True
        return False
