import time
import requests

from bs4 import BeautifulSoup

from fetchers.models.Job import Job
from utils.CleanUtils import CleanUtils
from fetchers.FetcherDocument import FetcherDocument
from fetchers.FetcherController import FetcherController


class YellowPagesFetcherController(FetcherController):
    MAX_PAGE_PER_SEARCH = 15
    BASE_URL = 'https://www.yellowpages.com/search?search_terms={category}&geo_location_terms={location}'
    CLASSES = {
        'results': 'result',
        'business_name': 'business-name',
        'phone': 'phones phone primary',
    }
    SOURCE = "YellowPages"

    def _read_web(self, job: Job, phones_to_ignore=None):

        # Change the job catehory if it has spaces
        job['category'] = job.get('category').replace(' ', "+")
        target_url = self.BASE_URL.format(**job)
        print(
            f"Attempting to crawl YellowPages using business: {target_url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
            "referer": target_url,
        }

        businesses = {}

        for i in range(0, self.MAX_PAGE_PER_SEARCH):
            url_with_page = f'{target_url}&page={i + 1}'
            result = requests.get(url_with_page, headers=headers)
            businesses |= self.extract_business(result.text)

            if not businesses:
                print("No business")
                break

        print(f"Bussines found: {len(businesses)}")

        if not businesses:
            return 0

        # Create the doc for each business
        docs = []
        for phone in businesses:
            url = businesses.get(phone)
            doc = self.make_crawler_document(phone, url, job)

            try:
                clean_phone = CleanUtils.clean_phone(phone)
                if not phones_to_ignore or clean_phone not in phones_to_ignore:
                    print(f"{phone} not int phones to ignore, getting HTML")
                    result = requests.get(
                        businesses[phone], headers=headers)

                    if result.status_code == 200:
                        doc.setData(result.text)
            except Exception as e:
                print(e)

            docs.append(doc)

        self.save(docs)

        return len(businesses)

    def extract_business(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        business = {}

        result_divs = soup.find_all('div', {'class': self.CLASSES['results']})

        for div in result_divs:
            anchor = div.find_all(
                'a', {'class': self.CLASSES['business_name']})
            phone = div.find_all(
                'div', {'class': self.CLASSES['phone']})

            if not phone:
                print('Business without phone number')
                continue

            url, phone = anchor.get('href'), phone.text

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
    job = {'country': 'USA', 'location': '92070',
           'category': 'Plumbing'}
    b = YellowPagesFetcherController()
    s = time.perf_counter()
    b._read_web(job)
    e = time.perf_counter()
    print(e-s)
