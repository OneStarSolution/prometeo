import psutil
import signal
import time
import requests

from concurrent.futures import ProcessPoolExecutor, as_completed

from bs4 import BeautifulSoup

from fetchers.models.Job import Job
from utils.CleanUtils import CleanUtils
from fetchers.FetcherDocument import FetcherDocument
from fetchers.FetcherController import FetcherController


class BBBFetcherController(FetcherController):
    MAX_PAGE_PER_SEARCH = 15
    BASE_URL = 'https://www.bbb.org/search?find_country={country}&find_loc={location}&find_text={category}'
    CLASSES = {
        'results': 'Content-ro0uyh-0 VyFaZ rresult-item-ab__content'
    }
    SOURCE = "BBB"

    def request_and_extract(self, i, target_url, headers):
        url_with_page = f'{target_url}&page={i + 1}'
        result = requests.get(url_with_page, headers=headers)
        businesses = self.extract_business(result.text)
        return businesses

    def _read_web(self, job: Job, phones_to_ignore=None):

        # Change the job catehory if it has spaces
        job['category'] = job.get('category').replace(' ', "+")
        target_url = self.BASE_URL.format(**job)
        print(
            f"Attempting to crawl BBB using URL: {target_url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
            "referer": target_url,
        }

        businesses = {}

        with ProcessPoolExecutor(max_workers=8) as pool:
            tasks = [pool.submit(self.request_and_extract, i, target_url, headers)
                     for i in range(0, self.MAX_PAGE_PER_SEARCH)]

            for task in as_completed(tasks):
                res = task.result()
                businesses |= res

        print(f"Bussines found: {len(businesses)}")

        if not businesses:
            return 0

        # Create the doc for each business
        docs = []

        for phone in businesses:
            url = businesses.get(phone)
            doc = self.make_crawler_document(phone, url, job)
            docs.append(doc)

        self.save(docs)

        return len(businesses)

    def extract_business(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        business = {}

        result_divs = soup.find_all('div', {'class': self.CLASSES['results']})

        for div in result_divs:
            anchors = div.find_all('a')

            if len(anchors) < 2:
                print('Business without phone number')
                continue

            url, phone = anchors[0].get('href'), anchors[1].text

            if phone and url:
                business[phone] = url

        return business

    def make_crawler_document(self, phone, url, job: Job):
        doc = FetcherDocument(phone, phone, url, job.get(
            'country'), job.get('location'))
        doc.category = job.get('category').replace('+', " ")
        doc.source = self.SOURCE
        return doc


def run_sample():
    job = {'country': 'USA', 'location': '96070',
           'category': 'Water Treatment'}
    b = BBBFetcherController()
    s = time.perf_counter()
    b._read_web(job)
    e = time.perf_counter()
    print(f"Time used: {e-s}")
