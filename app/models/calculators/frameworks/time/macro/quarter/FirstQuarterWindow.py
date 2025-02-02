# PM Macro
from datetime import datetime

from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


class FirstQuarterWindow(ITimeWindow):
    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_minute = time.minute

            if 40 >= current_minute >= 20:
                return True

            return False
        except Exception as e:
            logger.critical("Last Close Macro Exception", e)

