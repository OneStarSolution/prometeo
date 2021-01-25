import pandas as pd

from db.PrometeoDB import PrometeoDB


def getBusinesses(collection='yelp', query=None):
    with PrometeoDB() as db:
        yelp = db.get_yelp_business()
        query = {"location.country": "US"
                 } if not query else query
        result = [doc for doc in yelp.find(query)]
        df = pd.DataFrame(result)
        df.to_csv("YELP.csv")


getBusinesses()
