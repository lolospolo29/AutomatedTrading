from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


# PM Macro
class FirstCloseMacro(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_hour = time.hour
            current_minute = time.minute

            if 50 >= current_minute >= 10  and current_hour == 18 :
                return True

            return False
        except Exception as e:
            logger.critical("Time Window Exception {}".format(e))
