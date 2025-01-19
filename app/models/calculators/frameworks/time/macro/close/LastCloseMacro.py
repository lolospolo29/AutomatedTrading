# PM Macro
from datetime import datetime

from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


class LastCloseMacro(ITimeWindow):
    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_hour = time.hour
            current_minute = time.minute

            if 45 <= current_minute < 15 and current_hour == 20 :
                return True

            return False
        except Exception as e:
            logger.critical("Last Close Macro Exception", e)
        finally:
            return False


lcm = LastCloseMacro()
print(lcm.is_in_entry_window(datetime.now()))
