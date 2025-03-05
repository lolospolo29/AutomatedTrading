from app.interfaces.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


# SB Macro
class SilverBulletClose(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_hour = time.hour

            if 20 <= current_hour < 21 :
                return True

            return False
        except Exception as e:
            logger.critical("SilverBulletClose: Exception occurred ", e)
