import schedule

from app.monitoring.logging.logging_startup import logger
from app.services.NewsService import NewsService


class ScheduleService:

    def __init__(self):
        self._jobs:dict = {}
        self._news_service = NewsService()

        job =  schedule.every().saturday.at("12:00").do(self._news_service.run_news_scheduler)

        self._jobs["News"] = job

        for name, seconds in self._jobs.items():
            logger.info("Adding schedule for {}".format(name))

    @staticmethod
    def _add_tag(job, tag1:str=None, tag2:str=None):
        if tag1 is None:
            return job.tag(tag1)
        if tag2 is None:
            return job.tag(tag2)

    @staticmethod
    def _clear_one_time_jobs():
        schedule.clear("one_time")

    @staticmethod
    def start():
        while True:
            schedule.run_pending()

    @staticmethod
    def clear_by_tag(tag):
        schedule.clear(tag)

    def cancel_job(self,name):
        job = self._jobs[name]
        schedule.cancel_job(job)

    def get_jobs(self):
        return self._jobs.keys()

    def every_second_add_schedule(self,name:str,seconds:int,func,tag1:str=None,tag2:str=None):
        logger.info("Adding schedule for {}".format(name))
        if tag1 or tag2:
            job = self._add_tag(schedule.every(seconds).seconds.do(func),tag1,tag2)
            self._jobs[name] = job
        else:
            self._jobs[name] = schedule.every(seconds).seconds.do(func)

    def every_minute_add_schedule(self,name:str,minutes:int,func,tag1:str=None,tag2:str=None):
        logger.info("Adding schedule for {}".format(name))
        if tag1 or tag2:
            job = self._add_tag(schedule.every(minutes).minutes.do(func),tag1,tag2)
            self._jobs[name] = job
        else:
            self._jobs[name] = schedule.every(minutes).minutes.do(func)

    def every_hour_add_schedule(self,name,hours,func,tag1:str=None,tag2:str=None):
        logger.info("Adding schedule for {}".format(name))
        if tag1 or tag2:
            job = self._add_tag(schedule.every(hours).hours.do(func),tag1,tag2)
            self._jobs[name] = job
        else:
            self._jobs[name] = schedule.every(hours).hours.do(func)

    def every_day_add_schedule(self,name,time,func,tag1:str=None,tag2:str=None):
        logger.info("Adding schedule for {}".format(name))
        if tag1 or tag2:
            job = self._add_tag(schedule.every().day.at(time).do(func),tag1,tag2)
            self._jobs[name] = job
        else:
            self._jobs[name] = schedule.every().day.at(time).do(func)

    def every_specific_day_add_schedule(self,name,day,time,func,tag1:str=None,tag2:str=None):
        logger.info("Adding schedule for {}".format(name))
        job = None

        if day == "Monday":
            job = schedule.every().monday.at(time).do(func)
        if day == "Tuesday":
            job = schedule.every().tuesday.at(time).do(func)
        if day == "Wednesday":
            job = schedule.every().wednesday.at(time).do(func)
        if day == "Thursday":
            job = schedule.every().thursday.at(time).do(func)
        if day == "Friday":
            job = schedule.every().friday.at(time).do(func)
        if day == "Saturday":
            job = schedule.every().saturday.at(time).do(func)
        if day == "Sunday":
            job = schedule.every().sunday.at(time).do(func)

        if tag1 or tag2:
            job = self._add_tag(job,tag1,tag2)

        self._jobs[name] = job

    def every_x_between_add_schedule(self,func,name,repeating,between_from,between_to
                                     ,minutes:bool=True,seconds:bool=False
                                     ,hours:bool=False,day:bool=None,tag1:str=None,tag2:str=None):
        logger.info("Adding schedule for {}".format(name))

        job = None

        if minutes:
            job = schedule.every(repeating).minutes.between(between_from,between_to).do(func)
        if seconds:
            job = schedule.every(repeating).seconds.between(between_from,between_to).do(func)
        if hours:
            job = schedule.every(repeating).hours.between(between_from,between_to).do(func)
        if day:
            job = schedule.every(repeating).day.at(between_from).do(func)

        if tag1 or tag2:
            job = self._add_tag(job,tag1,tag2)

        self._jobs[name] = job


