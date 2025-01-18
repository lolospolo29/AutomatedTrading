from abc import ABC, abstractmethod


class ITimeWindow(ABC):  # Entry / Exit Times
    @abstractmethod
    def is_in_entry_window(self, time):
        pass

    @abstractmethod
    def is_in_exit_window(self, time):
        pass
