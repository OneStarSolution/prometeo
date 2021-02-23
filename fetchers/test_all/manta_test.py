from fetchers.test_all.url_scrapers.manta import MantaFetcherController
from fetchers.test_all.data_scrapers.manta_data_scraper import MantaDataScrape

with open('manta_test_url.txt', 'r') as f:
    urls = f.readlines()

for url in urls[:2]:
    html = MantaFetcherController(f"https://www.{url}")._read_web()
    doc = MantaDataScrape(html)
    doc.parse()
    print(doc.summary)
