import time
import requests

from bs4 import BeautifulSoup

from fetchers.models.Job import Job


class BBBFetcherController:
    MAX_PAGE_PER_SEARCH = 15
    BASE_URL = 'https://www.bbb.org/search?find_country={country}&find_loc={location}&find_text={category}'
    CLASSES = {
        'results': 'MuiGrid-root MuiGrid-container MuiGrid-align-items-xs-center'
    }

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

            # Get the html of every business
            htmls = {}
            for business in businesses:
                print(f"Getting HTML of {business}")
                result = requests.get(businesses[business], headers=headers)
                with open(f'{business}.html', 'w') as f:
                    f.write(result.text)
                htmls[business] = result.text

            # Create the doc for each business

            return len(businesses)
        except Exception as e:
            print(e)

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


job = {'country': 'USA', 'location': '96070', 'category': 'Water Treatment'}
b = BBBFetcherController()
s = time.perf_counter()
b._read_web(job)
e = time.perf_counter()
print(e-s)
