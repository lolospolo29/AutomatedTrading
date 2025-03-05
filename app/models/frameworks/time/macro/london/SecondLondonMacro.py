from app.interfaces.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


class SecondLondonMacro(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_hour = time.hour
            current_minute = time.minute

            if 33 > current_minute >= 3  and current_hour == 9:
                return True

            return False
        except Exception as e:
            logger.critical("Second London Macro exception {}".format(e))
