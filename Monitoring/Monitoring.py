from datetime import datetime


class Monitoring:
    @staticmethod
    def logInformation(info):
        print(datetime.now(), ":", info)
