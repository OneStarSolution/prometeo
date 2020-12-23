import os
import logging
import requests


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

        token = "L8G0jLGWzoQcJRTn4zmMoRJIWyB6yoO4X4Qf-V5xc5I6WSD6AC8V-XDWgoSr1JB__pBjcdKrvcQCLbQCSjTf0uwVmcQh0zXcdmAvmxiaqoPrGWnyVgmUGNq9bj3RX3Yx"
        headers = {"Authorization": f"Bearer {token}"}
        result = requests.get(self.url_base, params=params, headers=headers)

        return result.json().get('businesses', [])

    def business_in_db(self, category: str, location: str):
        return False
