import time
import datetime
import multiprocessing

from utils.yelp_token import get_tokens, get_yelp_token, get_token

from pydantic import HttpUrl

import requests

from db.PrometeoDB import PrometeoDB


TOO_MANY_REQUEST_ERROR_CODE = 429


class YELPClientController:
    SOURCE = "YELP"

    def __init__(self) -> None:
        self.BUSINESS_SEARCH_ENDPOINT = "https://api.yelp.com/v3/businesses/search"
        self.BUSINESS_DETAILS_ENDPOINT = "https://api.yelp.com/v3/businesses"

    def get(self, endpoint: HttpUrl, params: dict = None, headers: dict = None):
        # preparing request
        token_generator = get_yelp_token()
        # get a token assigned depending on process_number
        process_number = int(
            multiprocessing.current_process().name.split('-')[-1])
        token = get_token(process_number)
        print(f"Token: {process_number} - {token}")

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
        with PrometeoDB() as db:
            fetch_attempts_col = db.get_fetch_attempts()
            fetch_attempt_dict = {'SOURCE': self.SOURCE, "LOCATION": location,
                                  'CATEGORY': category, "TIME": datetime.datetime.now()}
            fetch_attempts_col.insert_one(fetch_attempt_dict)

        # logging.info(
        #     f"Attempting to crawl Yelp using Category: {category}, location: {location},\
        #       radius: {radius}")

        params = {
            'location': location,
            'term': category,
            'radius': radius
        }
        # get request
        result = self.get(self.BUSINESS_SEARCH_ENDPOINT, params=params)

        if not result:
            print("No results")
            return

        for business in result.json().get('businesses', []):
            print(
                f"Check business: {business.get('name')} ")

            # Skip business without phone numbers
            if not business.get('phone'):
                print("Skipping due to phone is missing")
                continue

            with PrometeoDB() as db:
                yelp_db = db.get_yelp_business()
                # check if exists
                query = {
                    'id': business.get('id')
                }
                business_on_db = yelp_db.find_one(query, {'_id': 1})
                # if so skip
                if business_on_db:
                    print(
                        f"Ignoring business: {business.get('name')} because it's already in the DB")
                    continue
                # else add it
                yelp_db.insert(business)
                print("SAVED!")

        return result.json().get('businesses', [])

    def fetch_business_details(self, business_id: str):
        print(
            f"Attempting to fetch business details from API: {business_id}")

        return self.get(f'{self.BUSINESS_DETAILS_ENDPOINT}/{business_id}')
