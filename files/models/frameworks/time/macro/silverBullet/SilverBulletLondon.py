from files.interfaces.ITimeWindow import ITimeWindow


# SB Macro
class SilverBulletLondon(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        current_hour = time.hour

        if 7 <= current_hour < 8:
            return True

        return False