from app.interfaces.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


class NYOpen(ITimeWindow):

    def is_in_exit_window(self, time) -> bool:
        return self.is_in_entry_window(time)

    @staticmethod
    def is_in_entry_window(time) -> bool:
        try:
            if  15 >= time.hour >= 12 :
                return True
            return False
        except Exception as e:
            logger.critical("Ny Open Error: {}".format(e))
