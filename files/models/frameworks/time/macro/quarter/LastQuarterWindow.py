from files.interfaces.ITimeWindow import ITimeWindow
from files.monitoring.logging.logging_startup import logger


class LastQuarterWindow(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_minute = time.minute

            if 0 <= current_minute <= 10 or 59 >= current_minute >= 50:
                return True

            return False
        except Exception as e:
            logger.critical("Last Close Macro Exception", e)
