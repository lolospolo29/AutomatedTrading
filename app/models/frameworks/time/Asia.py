from app.interfaces.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


class Asia(ITimeWindow):

    def is_in_exit_window(self, time) -> bool:
        return self.is_in_entry_window(time)

    @staticmethod
    def is_in_entry_window(time) -> bool:
        try:
            if  5 >= time.hour >= 0 :
                return True
            return False
        except Exception as e:
            logger.critical("Asia Session Error", e)
