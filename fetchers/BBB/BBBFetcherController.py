import time
import requests
from pydantic import HttpUrl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as expected_conditions

from fetchers.models.Job import Job


class BBBFetcherController:
    WAIT_ELEMENT = 20
    XPATHS = {}
    BASE_URL = 'https://www.bbb.org/search?find_country={country}&find_loc={location}&find_text={category}'

    def _read_web(self, job: Job):
        try:
            # Change the job catehory if it has spaces
            job['category'] = job.get('category').replace(' ', "+")
            target_url = self.BASE_URL.format(**job)
            print(
                f"Attempting to crawl BBB using business: {target_url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
                "referer": target_url,
            }

            result = requests.get(target_url, headers=headers)

            return result.text
        except Exception as e:
            print(e)


job = {'country': 'USA', 'location': '96070', 'category': 'Water Treatment'}
b = BBBFetcherController()
s = time.perf_counter()
b._read_web(job)
e = time.perf_counter()
print(e-s)
