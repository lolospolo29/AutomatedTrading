import re
from datetime import datetime
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from tools.EconomicScrapper.Models.NewsDay import NewsDay
from tools.EconomicScrapper.Models.NewsEvent import NewsEvent


class EconomicScrapper:
    def __init__(self):
        self.__options = Options()
        self.__service = \
            (Service('/Users/lauris/PycharmProjects/AutomatedTrading/tools/EconomicScrapper/chromedriver-mac-x64/chromedriver'))

        self.__driver = webdriver.Chrome(service=self.__service, options=self.__options)

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

            # Assign the UTC+1 timezone
            date_obj_utc_plus_1 = date_obj.replace(tzinfo=ZoneInfo("Europe/Berlin"))  # UTC+1 for Central European Time

            # Return the date in ISO format
            return date_obj_utc_plus_1.isoformat()

        return None  # Return None if no date found

    def returnCalendar(self)->list[NewsDay]:
        newsDays = []
        try:
            # Open the website
            url = "https://tradingeconomics.com/calendar"  # Replace with the target website URL
            self.__driver.get(url)
            WebDriverWait(self.__driver, 10)

            # Find the button with the specific ID and click it
            button = self.__driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ctl02_Button1")  # Replace 'your-button-id' with the actual button ID
            button.click()
            print("Button clicked successfully!")

            WebDriverWait(self.__driver, 10)

            checkbox_input = self.__driver.find_element(By.XPATH,
                                                 "/html/body/form/div[3]/div/div/table/tbody/tr/td[1]/div/div[2]/ul/li[2]/a/input")
            if not checkbox_input.is_selected():  # If it's not selected, click to select it
                checkbox_input.click()
                print("Checkbox selected!")


            event_elements = self.__driver.find_elements(By.CSS_SELECTOR, "tr")

            currentNewsDay:NewsDay = None
            # Process each event and check for timestamp
            for index, event in enumerate(event_elements):

                event_text = event.text.strip()

                date = self._extract_date_from_event(event_text)

                if not date is None:
                    newsDay = NewsDay(date,[])
                    newsDays.append(newsDay)
                    currentNewsDay = newsDay

                # Extract time and daytime (AM/PM)
                time_obj, daytime = self._extract_time_and_daytime(event_text)

                if time_obj and daytime:
                    title, currency = self._extract_title_and_currency(event_text)

                    # Create NewsEvent dataclass and append to list
                    news_event = NewsEvent(time=time_obj, title=title, currency=currency, daytime=daytime)
                    currentNewsDay.newsEvents.append(news_event)
            try:
                for newsDay in newsDays:
                    print()
                    print(f"Appended NewsEvent {newsDay.dayIso}")
                    for newsEvent in newsDay.newsEvents:
                        print(f"Appended NewsEvent {newsEvent.title}")
                    print()
            except:
                print(newsDays)

        finally:
            # Close the WebDriver
            self.__driver.quit()
            return newsDays
