import time
import pandas as pd

from fetchers.yelp.YELPFetcherController import YELPFetcherController
from fetchers.yelp.YELPFetcherDocument import YELPFetcherDocument
from fetchers.yelp.YELPClientController import YELPClientController


url = 'https://www.yelp.com/biz/whitehorse-plumbing-albuquerque-2'
url_2 = 'https://www.yelp.com/biz/lawson-family-plumbing-phoenix'


def YELPController_run_sample():
    f = YELPFetcherController(url)
    html = f._read_web()

    d = YELPFetcherDocument(url)
    d.setData(html)

    df = pd.DataFrame([vars(d)])
    df.to_csv("test.csv")


def YELPClient_run_sample(category: str, location: str):
    try:
        c = YELPClientController()
        business = c.fetch(category, location)

        if not business:
            print(f"There're no business in this area: {location}")
            return 1

        df = pd.DataFrame(business)
        df.to_csv(f"yelp_data/{category}_{location}.csv")
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


run()
