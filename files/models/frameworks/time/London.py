from files.interfaces.ITimeWindow import ITimeWindow

class LondonOpen(ITimeWindow):

    def is_in_exit_window(self, time) -> bool :
        return self.is_in_entry_window(time)

    @staticmethod
    def is_in_entry_window(time) -> bool:
            if  9 >= time.hour >= 6 :
                return True
            return False