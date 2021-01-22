import time
import datetime
import multiprocessing

from utils.yelp_token import get_tokens, get_yelp_token, get_token

from pydantic import HttpUrl
from pymongo.errors import BulkWriteError

import requests

from db.PrometeoDB import PrometeoDB


TOO_MANY_REQUEST_ERROR_CODE = 429


class YELPClientController:
    SOURCE = "YELP"
    LIMIT_RESULTS = 50

    def __init__(self) -> None:
        self.BUSINESS_SEARCH_ENDPOINT = "https://api.yelp.com/v3/businesses/search"
        self.BUSINESS_DETAILS_ENDPOINT = "https://api.yelp.com/v3/businesses"

    def get(self, endpoint: HttpUrl, params: dict = None, headers: dict = None):
        # preparing request
        token_generator = get_yelp_token()
        # get a token assigned depending on process_number
        process_name = multiprocessing.current_process().name
        process_number = int(process_name.split(
            '-')[-1]) if process_name != "MainProcess" else 1
        token = get_token(process_number)

        bearer_token = {"Authorization": f"Bearer {token}"}

        headers = headers | bearer_token if headers else bearer_token

        # get request
        result = requests.get(endpoint, params=params, headers=headers)

        # Swith token if 429 error is returned by the API
        NUMBER_YELP_API_TOKENS = len(get_tokens())
        for _ in range(NUMBER_YELP_API_TOKENS):
            if result.status_code == TOO_MANY_REQUEST_ERROR_CODE:
                print(
                    f'Changing token because {result.json().get("error").get("code")}')
                time.sleep(1)

                try:
                    token = next(token_generator)
                    bearer_token = {"Authorization": f"Bearer {token}"}
                    headers = headers | bearer_token if headers else bearer_token
                except StopIteration:
                    print("All the tokens have been used. Exiting!")
                    return

                result = requests.get(endpoint, params=params, headers=headers)
            # Token was changed so break loop
            else:
                break

        return result

    def fetch(self, category: str, location: str, radius: int = 40000):
        start_time = time.perf_counter()

        with PrometeoDB() as db:
            fetch_attempts_col = db.get_fetch_attempts()
            fetch_attempt_dict = {'SOURCE': self.SOURCE, "LOCATION": location,
                                  'CATEGORY': category, "TIME": datetime.datetime.now()}
            fetch_attempts_col.insert_one(fetch_attempt_dict)

        print(
            f"Attempting to crawl Yelp using Category: {category}, location: {location}, radius: {radius}")

        params = {
            'location': location,
            'term': category,
            'radius': radius,
            'limit': self.LIMIT_RESULTS,
            'offset': 0
        }
        # get request
        result = self.get(self.BUSINESS_SEARCH_ENDPOINT, params=params)
        total = result.json().get('total', 0)
        businesses = []
        number_request = 1

        print(f"Found {total // self.LIMIT_RESULTS} pages")

        for offset in range(self.LIMIT_RESULTS, total, self.LIMIT_RESULTS):
            print(f'Page: {offset // self.LIMIT_RESULTS}')
            businesses.extend(result.json().get('businesses', []))

            # get request
            params |= {'offset': offset}
            result = self.get(self.BUSINESS_SEARCH_ENDPOINT, params=params)
            number_request += 1

        with PrometeoDB() as db:
            businesses_to_insert = []
            yelp_db = db.get_yelp_business()

            businesses_ids = [business.get('id') for business in businesses]
            # check if exists
            query = {
                'id': {"$in": businesses_ids}
            }
            business_on_db = yelp_db.find(query, {'id': 1})

            if business_on_db:
                business_on_db = set(business_on_db)

            for business in businesses:
                # Skip business without phone numbers
                if not business.get('phone'):
                    print("Skipping due to phone is missing")
                    continue

                # if so skip
                if business.get('id') in business_on_db:
                    continue

                # else add it
                businesses_to_insert.append(business)

            try:
                if businesses_to_insert:
                    yelp_db.insert_many(
                        businesses_to_insert, ordered=False)

                print(
                    f"---Total Business in {location}---\
                        Found: {len(businesses)}\
                            Inserted: {len(businesses_to_insert)}\
                                Duplicated: {len(businesses) - len(businesses_to_insert)}")

            except BulkWriteError as e:
                print(f"MONGO ERROR: {e}")

        if not businesses:
            print("NO RESULTS")

        with PrometeoDB() as db:
            businesses_to_insert = []
            zipcodes = db.get_request_zipcodes()
            doc = {
                'crawl_time': time.perf_counter() - start_time,
                'radius': radius,
                'location': location,
                'source': self.SOURCE,
                'category': category,
                'requests': number_request,
                'found': len(businesses),
                'inserted': len(businesses_to_insert),
                'duplicates': len(businesses) - len(businesses_to_insert),
            }
            zipcodes.insert(doc)

        return businesses

    def fetch_business_details(self, business_id: str):
        print(
            f"Attempting to fetch business details from API: {business_id}")

        return self.get(f'{self.BUSINESS_DETAILS_ENDPOINT}/{business_id}')
