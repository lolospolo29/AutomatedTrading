from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


# Lunch Macro
class LunchNYMacro(ITimeWindow):
    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_hour = time.hour
            current_minute = time.minute

            if (50 <= current_minute  and current_hour == 16) or (10 >= current_minute and current_hour == 17) :
                return True

            return False
        except Exception as e:
            logger.critical("Lunch NY Macro Exception {}".format(e))
