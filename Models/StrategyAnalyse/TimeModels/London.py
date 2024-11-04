from datetime import datetime

import pytz

from Interfaces.RiskManagement.ITimeWindow import ITimeWindow

berlinTimezone = pytz.timezone('Europe/Berlin')


class LondonOpen(ITimeWindow):
    def IsInExitWindow(self) -> bool :
        # Get the current time in Berlin
        currentTimeBerlin = datetime.now(berlinTimezone)

        # Check if the current hour is 12 (noon)
        if currentTimeBerlin.hour == 17:
            return True
        return False

    def IsInEntryWindow(self) -> bool:
        # Get the current time in Berlin
        currentTimeBerlin = datetime.now(berlinTimezone)

        # Check if the current hour is between 8 AM and 11 AM (inclusive)
        if 8 <= currentTimeBerlin.hour <= 11:
            return True
        return False
