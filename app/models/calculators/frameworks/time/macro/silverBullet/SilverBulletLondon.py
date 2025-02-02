from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


# SB Macro
class SilverBulletLondon(ITimeWindow):
    def is_in_exit_window(self, time):
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time):
        try:
            current_hour = time.hour

            if 8 <= current_hour < 9 :
                return True

            return False
        except Exception as e:
            logger.critical("Silver Bullet London Exception", e)
