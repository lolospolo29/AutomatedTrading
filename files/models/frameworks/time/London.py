from files.interfaces.ITimeWindow import ITimeWindow
from files.monitoring.logging.logging_startup import logger


class LondonOpen(ITimeWindow):

    def is_in_exit_window(self, time) -> bool :
        return self.is_in_entry_window(time)

    @staticmethod
    def is_in_entry_window(time) -> bool:
        try:
            if  10 >= time.hour >= 7 :
                return True
            return False
        except Exception as e:
            logger.critical("London Open Error", e)
