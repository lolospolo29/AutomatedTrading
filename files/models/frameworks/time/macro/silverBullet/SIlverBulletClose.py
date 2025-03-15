from files.interfaces.ITimeWindow import ITimeWindow


# SB Macro
class SilverBulletClose(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        current_hour = time.hour

        if 18 <= current_hour < 19:
            return True

        return False