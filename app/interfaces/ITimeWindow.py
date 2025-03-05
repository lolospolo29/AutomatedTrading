from abc import ABC


class ITimeWindow(ABC):

    @staticmethod
    def is_in_exit_window(self, time) -> bool :
        pass

    @staticmethod
    def is_in_entry_window(time) -> bool:
        pass
