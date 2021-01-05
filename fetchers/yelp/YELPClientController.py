import os
import logging

import requests

from db.PrometeoDB import PrometeoDB
from utils.environment import get_yelp_token, NUMBER_YELP_API_TOKENS


TOO_MANY_REQUEST_ERROR_CODE = 429


class YELPClientController:

    def __init__(self) -> None:
        self.url_base = "https://api.yelp.com/v3/businesses/search"

    def fetch(self, category: str, location: str, radius: int = 12875):

        if self.business_in_db(category, location):
            return

        logging.info(
            f"Attempting to crawl Yelp using Category: {category}, location: {location},\
              radius: {radius}")

        params = {
            'location': location,
            'term': category,
            'radius': radius
        }

        # preparing request
        token_generator = get_yelp_token()
        token = next(token_generator)
        headers = {"Authorization": f"Bearer {token}"}
        # get request
        result = requests.get(self.url_base, params=params, headers=headers)

        # Swith token if 429 error is returned by the API
        for i in range(NUMBER_YELP_API_TOKENS):
            print("entre", result.status_code, result)
            if result.status_code == TOO_MANY_REQUEST_ERROR_CODE:
                print(f'Changing token because ACCESS_LIMIT_REACHED')

                try:
                    token = next(token_generator)
                    headers = {"Authorization": f"Bearer {token}"}
                except StopIteration:
                    print("All the tokens have been used. Exiting!")
                    return

                result = requests.get(
                    self.url_base, params=params, headers=headers)
            # Token was changed so break loop
            else:
                break

        i = 0
        for business in result.json().get('businesses', []):
            print(
                f"Check business: {business.get('name')} ")

            if i > 2:
                break
            i += 1
            # Skip business without phone numbers
            if not business.get('phone'):
                continue

            with PrometeoDB() as db:
                yelp_db = db.get_yelp_business()
                # check if exists
                query = {
                    'phone': business.get('phone')
                }
                business_on_db = yelp_db.find_one(query, {'_id': 1})
                # if so skip
                if business_on_db:
                    print(
                        f"Ignoring business: {business.get('name')} because it's already in the DB")
                    continue
                # else add it
                yelp_db.insert(business)
                # jOHNs -> 2020
                # jOHNs -> 2021

        return result.json().get('businesses', [])

    def business_in_db(self, category: str, location: str):
        return False
