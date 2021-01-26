from pymongo import MongoClient

from utils.environment import NOSQL_USER, NOSQL_PASS, get_mongo_url


# DBs
PROMETEO_DB = "prometeo_db"

# Collections
YELP = "yelp"
FETCH_ATTEMPTS = "fetch_attempts"
REQUEST_ZIPCODES = "requests_zipcodes"


class PrometeoDB:

    def __init__(self, **kwargs):
        self.mongo_client = MongoClient(
            get_mongo_url(),
            username=NOSQL_USER,
            password=NOSQL_PASS
        )

        self.prometeo_db = self.mongo_client[PROMETEO_DB]

    def get_yelp_business(self):
        return self.prometeo_db[YELP]

    def get_fetch_attempts(self):
        return self.prometeo_db[FETCH_ATTEMPTS]

    def get_request_zipcodes(self):
        return self.prometeo_db[REQUEST_ZIPCODES]

    def close(self):
        if self.mongo_client is not None:
            self.mongo_client.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __enter__(self):
        return self
