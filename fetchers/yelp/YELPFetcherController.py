import logging
from pydantic import HttpUrl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as expected_conditions


class YELPFetcherController:
    WAIT_ELEMENT = 20
    XPATHS = {
        'title': "/html/body/div[2]/div[3]/yelp-react-root/div/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/h1"
    }

    def __init__(self, url: HttpUrl) -> None:
        chrome_options = Options()
        chrome_options.headless = True
        self.driver = webdriver.Chrome(
            executable_path="drivers/chromedriver", options=chrome_options)
        self.url_base = url

    def _read_web(self):
        # Delete cookies
        self.driver.delete_all_cookies()

        logging.info(
            f"Attempting to crawl Yelp using business: {self.url_base}")

        # As YELP don't use to fail just try to connect directly
        self.driver.get(self.url_base)

        try:
            # Wait for title be displayed
            WebDriverWait(self.driver, self.WAIT_ELEMENT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, self.XPATHS.get('title'))
                )
            )
        except TimeoutException:
            logging.info("Title is not in the screen after wait. Aborting!")
            return None

        return self.driver.page_source