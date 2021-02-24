from fetchers.test_all.url_scrapers.manta import MantaFetcherController
from fetchers.test_all.data_scrapers.manta_data_scraper import MantaDataScrape

with open('manta_test_url.txt', 'r') as f:
    urls = f.readlines()

for url in urls[:2]:
    url = f"https://www.{url}"
    print(f"url: {url}")
    html = MantaFetcherController(url)._read_web()
    if html:
        print("creating doc")
        doc = MantaDataScrape(html)
        doc.parse()
        print(doc.summary)
