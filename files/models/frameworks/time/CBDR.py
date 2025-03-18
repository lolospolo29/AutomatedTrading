from files.interfaces.ITimeWindow import ITimeWindow

class CBDRPM(ITimeWindow):

    @property
    def name(self):
        return "CBDR"

    def is_in_exit_window(self, time) -> bool :
        return self.is_in_entry_window(time)

    @staticmethod
    def is_in_entry_window(time) -> bool:
            if  18 >= time.hour >= 24  :
                return True
            return False