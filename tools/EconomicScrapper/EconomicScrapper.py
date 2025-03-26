import re
from datetime import datetime,timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from logging import Logger


from files.helper.functions.to_utc import to_utc
from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent

class EconomicScrapper:
    """
    Scrapes economic calendar data from TradingEconomics.com to extract information on news events and dates.
    It processes event data to create structured objects with details like time, title, currency, and timezone adjustments.
    The output is a list of NewsDay objects, each containing relevant news events for a specific day.
    """

    def __init__(self, logger:Logger):
        self.__driver = None
        self.__logger = logger

    @staticmethod
    def _extract_time_and_daytime(event_text):
        """
        Extracts time and daytime (AM/PM) from the event text in the format `hh:mm AM/PM`.
        """
        # Regular expression to match time (e.g., 7:00 AM or 1:12 PM)
        time_pattern = r'(\d{1,2}:\d{2})\s?(AM|PM)'
        match = re.search(time_pattern, event_text)

        if match:
            time_str = match.group(1)
            daytime = match.group(2)
            time_obj = datetime.strptime(time_str, "%I:%M")  # Convert time string to datetime object
            time_obj = time_obj.replace(tzinfo=timezone.utc)
            time_obj = to_utc(time_obj)
            return time_obj, daytime
        return None, None  # Return None if no match found

    @staticmethod
    def _extract_title_and_currency(event_text):
        """
        Extracts the event title and currency from the event text.
        This assumes the currency comes after the time (e.g., 'US') and the title comes after that.
        """
        # Split the text based on spaces
        parts = event_text.split()

        # The second part is assumed to be the currency (e.g., 'US')
        currency = parts[2] if len(parts) > 2 and parts[2].isalpha() else ""

        # The title is everything after the currency part
        title = " ".join(parts[3:]) if currency else event_text

        return title.strip(), currency.strip()

    # noinspection GrazieInspection
    @staticmethod
    def _extract_date_from_event(event_text):
        """
        Extracts and returns the date in ISO format ('YYYY-MM-DDTHH:MM:SS+01:00') from the event text.
        The date format should be 'Day Month DayNumber Year' (e.g., 'Monday January 06 2025').
        """
        # Regular expression to match 'Day Month DayNumber Year'
        date_pattern = r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) ' \
                       r'(?:January|February|March|April|May|June|July|August|September|October|November|December) ' \
                       r'\d{1,2} \d{4}\b'

        # Search for the date pattern in the text
        match = re.search(date_pattern, event_text)
        if match:
            # Extracted date string (e.g., "Monday January 06 2025")
            date_str = match.group()

            # Convert it into a datetime object
            date_obj = datetime.strptime(date_str, "%A %B %d %Y")
            date_obj = date_obj.replace(tzinfo=timezone.utc)
            date_obj = to_utc(date_obj)
            # Return the date in ISO format
            return date_obj

        return None  # Return None if no date found

    def return_calendar(self) -> list[NewsDay]:
        """
        Scrapes the economic calendar from TradingEconomics.com and returns a list of NewsDay objects.
        Each NewsDay contains news events with details like time, title, currency, and adjusted timezone information.
        """

        news_days = []
        try:
            self.__driver = webdriver.Chrome()
            # Open the website
            url = "https://tradingeconomics.com/calendar"  # Replace with the target website URL
            self.__driver.get(url)
            WebDriverWait(self.__driver, 10)

            # Find the button with the specific ID and click it
            button = self.__driver.find_element(By.ID,
                                                "ctl00_ContentPlaceHolder1_ctl02_Button1")  # Replace 'your-button-strategy_id' with the actual button ID
            button.click()

            WebDriverWait(self.__driver, 10)

            checkbox_input = self.__driver.find_element(By.XPATH,
                                                        "/html/body/form/div[3]/div/div/table/tbody/tr/td[1]/div/div[2]/ul/li[3]/a/input")
            if not checkbox_input.is_selected():  # If it's not selected, click to select it
                checkbox_input.click()

            button = self.__driver.find_element(By.ID,
                                                "DropDownListTimezone")  # Replace 'your-button-strategy_id' with the actual button ID
            button.click()
            WebDriverWait(self.__driver, 3)

            checkbox_input = self.__driver.find_element(By.XPATH,
                                                        "/html/body/form/div[3]/div/div/table/tbody/tr/td[1]/div/div[4]/div/select/option[13]")
            if not checkbox_input.is_selected():  # If it's not selected, click to select it
                checkbox_input.click()
            WebDriverWait(self.__driver, 3)

            event_elements = self.__driver.find_elements(By.CSS_SELECTOR, "tr")

            current_news_day: [NewsDay] = None
            self.__logger.debug(event_elements)
            # Process each event and check for timestamp
            for index, event in enumerate(event_elements):
                try:
                    event_text = event.text.strip()

                    date = self._extract_date_from_event(event_text)
                    if not date is None:
                        news_day = NewsDay(day_iso=date, news_events=[])
                        news_days.append(news_day)
                        current_news_day = news_day

                    # Extract time and daytime (AM/PM)
                    time_obj, daytime = self._extract_time_and_daytime(event_text)
                    if time_obj and daytime:
                        title, currency = self._extract_title_and_currency(event_text)

                        # Create NewsEvent dataclass and append to list
                        news_event = NewsEvent(time=time_obj, title=str(title), currency=str(currency), daytime=daytime)
                        current_news_day.news_events.append(news_event)
                except Exception as e:
                    self.__logger.critical("NewsDay exception: {}".format(e))
                for news_day in news_days:
                    try:
                        # Convert newsDay.dayIso to a datetime object (without time)
                        day_date = news_day.day_iso
                        time_obj = None
                        for news_event in news_day.news_events:
                            # Ensure newsEvent.time is a string and convert to a time object
                            if isinstance(news_event.time, str):
                                time_obj = datetime.strptime(news_event.time, "%H:%M:%S").time()
                            elif isinstance(news_event.time, datetime):
                                time_obj = news_event.time.time()

                                # If PM, add 12 hours to the time (except for 12 PM which is already correct)
                            if time_obj:
                                if time_obj.hour == 0:
                                    time_obj = time_obj.replace(hour=time_obj.hour + 12)

                            # Combine the date from newsDay and time from newsEvent
                            combined_datetime = datetime.combine(day_date, time_obj)

                            combined_datetime = combined_datetime.replace(tzinfo=timezone.utc)

                            combined_datetime_with_tz = to_utc(combined_datetime)

                            # Now, combined_datetime_with_tz is in UTC+1
                            news_event.time = combined_datetime_with_tz
                    except Exception as e:
                        self.__logger.critical("NewsEvents exception: {}".format(e))
        except Exception as e:
            self.__logger.critical("Trading Econmocis fetching exception: {}".format(e))
        finally:
            # Close the WebDriver
            self.__driver.quit()
            self.__logger.info("Finished scraping Economic Scraper,Found {} news days.".format(len(news_days)))
            return news_days