import time
import requests

from bs4 import BeautifulSoup

from fetchers.models.Job import Job
#from utils.CleanUtils import CleanUtils
#from fetchers.FetcherDocument import FetcherDocument
#from fetchers.FetcherController import FetcherController
from fetchers.test_all.utils.duplicate_checker import duplicate_checker


class BBBFetcherController():
    MAX_PAGE_PER_SEARCH = 15
    BASE_URL = 'https://www.bbb.org/search?find_country={country}&find_loc={location}&find_text={category}'
    CLASSES = {
        'results': 'Content-ro0uyh-0 iFxxPD rresult-item-ab__content'
    }
    SOURCE = "BBB"

    def _read_web(self, job: Job, phones_to_ignore=None):

        # Change the job catehory if it has spaces
        job['category'] = job.get('category').replace(' ', "+")
        target_url = self.BASE_URL.format(**job)
        print(
            f"Attempting to crawl BBB using business: {target_url}")

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
            # return 0
            return [{}]

        # Create the doc for each business
        docs = []
        for phone in businesses:
            url = businesses.get(phone)

            source_url = url
            source_url = source_url.split("https://")[1]
            if '?' in source_url:
                source_url = source_url.split("?")[0]

            url_status = duplicate_checker('bbb url', url)
            if url_status:
                status = duplicate_checker('phone', phone.replace("-", ""))
                if status:
                    new_lead_dict = {}
                    new_lead_dict["bbb url"] = source_url
                    new_lead_dict["phone"] = phone.replace("-", "")
                    docs.append(new_lead_dict)

            # Uncomment when you want to store in a db
            # doc = self.make_crawler_document(phone, url, job)

            # try:
            #     clean_phone = CleanUtils.clean_phone(phone)
            #     if not phones_to_ignore or clean_phone not in phones_to_ignore:
            #         print(f"{phone} not int phones to ignore, getting HTML")
            #         result = requests.get(
            #             businesses[phone], headers=headers)

            #         if result.status_code == 200:
            #             doc.setData(result.text)
            # except Exception as e:
            #     print(e)

        # Uncomment when you want to store in a db
        # self.save(docs)

        # return len(businesses)
        return docs

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


# job = {'country': 'USA', 'location': '96070', 'category': 'Water Treatment'}
# b = BBBFetcherController()
# s = time.perf_counter()
# b._read_web(job)
# e = time.perf_counter()
# print(e-s)
