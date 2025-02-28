from app.interfaces.framework.ITimeWindow import ITimeWindow
from app.monitoring.logging.logging_startup import logger


class LondonOpen(ITimeWindow):
    def to_dict(self):
        pass

    def is_in_exit_window(self, time) -> bool :
        return self.is_in_entry_window(time)

    def is_in_entry_window(self, time) -> bool:
        try:
            if  10 >= time.hour >= 7 :
                return True
            return False
        except Exception as e:
            logger.critical("London Open Error", e)
