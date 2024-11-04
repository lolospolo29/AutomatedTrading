from datetime import datetime

import pytz

from Interfaces.RiskManagement.ITimeWindow import ITimeWindow

berlinTimezone = pytz.timezone('Europe/Berlin')


class LondonMacroFX(ITimeWindow):
    def IsInExitWindow(self):
        pass

    def IsInEntryWindow(self):
        currentTimeBerlin = datetime.now(berlinTimezone)

        # Check if the current time is between 8:33 and 9:00 or 10:03 and 10:30
        if (currentTimeBerlin.hour == 8 and currentTimeBerlin.minute >= 33) or \
            (currentTimeBerlin.hour == 9 and currentTimeBerlin.minute == 0) or \
            (currentTimeBerlin.hour == 10 and currentTimeBerlin.minute < 30 and currentTimeBerlin.minute >= 3):
            return True

        return False
