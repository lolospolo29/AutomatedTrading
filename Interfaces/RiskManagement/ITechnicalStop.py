from abc import ABC, abstractmethod


class ITechnicalStop(ABC): # dynamisch oder statisch gehandhabt wird (z.B. Trailing Stop, Steady Stop Loss,
    # Break-Even).
    @abstractmethod
    def moveExit(self):  # return list of possible exits
        pass

