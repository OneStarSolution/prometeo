import math
import time
import pandas as pd

from math import ceil
from concurrent.futures import ProcessPoolExecutor

from fetchers.yelp.YELPFetcherController import YELPFetcherController
from fetchers.yelp.YELPFetcherDocument import YELPFetcherDocument
from fetchers.yelp.YELPClientController import YELPClientController


url = 'https://www.yelp.com/biz/whitehorse-plumbing-albuquerque-2'
url_2 = 'https://www.yelp.com/biz/lawson-family-plumbing-phoenix'


def YELPController_run_sample(url):
    d = {}
    try:
        f = YELPFetcherController(url)
        html = f._read_web()

        d = YELPFetcherDocument(url)
        d.setData(html)

        # df = pd.DataFrame([vars(d).get('summary', {})])
        # df.to_csv("test.csv")
    except Exception as e:
        print(e)
    finally:
        return vars(d).get('summary', {})


def YELPClient_run_sample(category: str, location: str):
    try:
        c = YELPClientController()
        business = c.fetch(category, location)

        if not business:
            print(f"There're no business in this area: {location}")
            return 1

        return 1
    except Exception as e:
        print(e)
        # error
        return 0


def run():
    category = input("Type the category you would like to crawl: ")
    category_in_file = category.replace(' ', '_')

    filename = f'{category_in_file}_yelp_zipcodes.csv'

    df = pd.read_csv(filename)

    for i, (zipcode, status) in df.iterrows():
        try:
            print(f"Crawling {zipcode}")
            if status != 0:
                print(f"Skipping zipcode {zipcode} because it was processed")
                continue

            success = YELPClient_run_sample(category, zipcode)
            if success:
                df.at[i, 'status'] = 1
        finally:
            df.to_csv(filename, index=False)

        time.sleep(1)


def run_yelpfc_parallel(url):
    url = f'https://www.yelp.com/{url}'
    print(url)
    try:
        doc = YELPController_run_sample(url.strip().replace('\n', ''))
        doc['original_url'] = url
        return doc
    except Exception as e:
        return {}


def run_yelpfc_parallel_chunk():
    # read file
    urls = pd.read_csv('urls.csv')['source_url'][2500:4000]

    workers = 4
    urls_docs = []

    try:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    run_yelpfc_parallel, url) for url in urls
            ]

        for future in futures:
            res = future.result()
            if res:
                urls_docs.append(res)

    except Exception as e:
        print(e)
    finally:
        df = pd.DataFrame(urls_docs)
        df.to_csv("urls_crawled.csv")


def run_yelpfc_seq():
    # read file
    urls = pd.read_csv('urls.csv')['source_url'][:8]
    docs = []
    for url in urls:
        url = f'https://www.yelp.com/{url}'
        print(url)
        try:
            doc = YELPController_run_sample(url.strip().replace('\n', ''))
        except Exception as e:
            continue
        doc['original_url'] = url
        if doc:
            docs.append(doc)
    df = pd.DataFrame(docs)
    df.to_csv("urls_crawled.csv")
    return docs


# print(run_yelpfc_seq())
s = time.perf_counter()
run_yelpfc_parallel_chunk()
print("total_time: ", time.perf_counter() - s)
# print((YELPController_run_sample(
#     'https://www.yelp.com/biz/j-and-m-construction-services-dover')))
