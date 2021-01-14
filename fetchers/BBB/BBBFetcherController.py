import logging
import time
from pydantic import HttpUrl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as expected_conditions


class BBBFetcherController:
    WAIT_ELEMENT = 20
    XPATHS = {}
    BASE_URL = ""

    def _read_web(self):
        try:
            # Delete cookies
            self.driver.delete_all_cookies()

            logging.info(
                f"Attempting to crawl BBB using business: {self.url_base}")

            # As BBB don't use to fail just try to connect directly
            self.driver.get(self.BASE_URL)

            # CODE HERE

            return self.driver.page_source
        except Exception as e:
            print(e)
        finally:
            self.driver.close()
